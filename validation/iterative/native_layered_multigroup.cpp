// Physical fixed-source columns with independent regional/layer totals.
// Include the unchanged old implementation to expose its two regression ABIs.
#include "native_layered_transport.cpp"

namespace {
int multigroup_core(int nr,int nz,int k,const double* widths,
  const int* regions,const double* total,int entry_surface,double H,double mu,
  int orientation,int order,const double* gn,const double* gw,const double* q,
  const double* radial_in,const double* axial_in,double* geometric,
  double* fields,double* metrics) {
  constexpr int nm=27;
  if(nr<1||nr>15||nz<1||nz>64||k<1||k>370||!(H>0)||!std::isfinite(H)||
     !(std::abs(mu)>0&&std::abs(mu)<1)||order<2||order>128||
     (orientation!=1&&orientation!=-1)||entry_surface<0||entry_surface>=6)
    return -1;
  if(!widths||!regions||!total||!gn||!gw||!q||!radial_in||!axial_in||
     !geometric||!fields||!metrics)return -7;
  for(int i=0;i<nr;++i)
    if(!(widths[i]>0)||!std::isfinite(widths[i])||regions[i]<0||regions[i]>=8)
      return -2;
  for(int i=0;i<8*nz*k;++i)
    if(total[i]<0||!std::isfinite(total[i])||!std::isfinite(q[i]))return -3;
  for(int i=0;i<6*nz*k;++i)if(!std::isfinite(radial_in[i]))return -3;
  for(int i=0;i<8*k;++i)if(!std::isfinite(axial_in[i]))return -3;
  for(int i=0;i<order;++i)
    if(!(gn[i]>-1&&gn[i]<1)||!(gw[i]>0)||!std::isfinite(gw[i]))return -3;
  Geo g;std::vector<double> lengths;
  // The original 113-bit geometry is constructed once for all k columns.
  int rc=make_layered_geo(widths,nr,H,nz,mu,orientation,order,gn,gw,g,lengths);
  if(rc)return rc;
  const int nc=nr*nz;
  std::fill(fields,fields+nc*9*k,0.);std::fill(metrics,metrics+k*nm,0.);
  geometric[0]=g.br.size()-1;geometric[1]=g.chords;geometric[2]=g.pieces.size();
  geometric[3]=0.;geometric[4]=std::numeric_limits<double>::infinity();geometric[5]=0.;
  for(size_t i=0;i<g.pieces.size();++i)
    geometric[4]=std::min(geometric[4],lengths[i]);
  for(int i=0;i<nr;++i)for(int j=0;j<nz;++j) {
    const double dz=g.z[j+1]-g.z[j];
    geometric[5]=std::max(geometric[5],ratio(g.x[i+1]-g.x[i]-g.w[i],g.w[i]));
    for(int f=0;f<9;++f) {
      double expected=0.;
      if(f==0)expected=g.w[i]*dz;
      else {
        int side=(f-1)%4;
        bool incoming=side==(orientation==1?0:1)||side==(mu>0?2:3);
        if((f<5&&incoming)||(f>=5&&!incoming))
          expected=side<2?dz:std::abs(mu)*g.w[i];
      }
      geometric[3]=std::max(geometric[3],ratio(g.raw[(i*nz+j)*9+f]-expected,expected));
    }
  }
  for(int c=0;c<k;++c) {
    double* m=metrics+c*nm;
    m[0]=m[1]=std::numeric_limits<double>::infinity();m[2]=m[12]=-1.;
  }
  std::vector<double> state(k);int ray=-1;
  for(size_t index=0;index<g.pieces.size();++index) {
    const auto& p=g.pieces[index];int i=p.cell/nz,j=p.cell%nz,r=regions[i];
    const double l=lengths[index];const double* source=q+(r*nz+j)*k;
    if(ray!=p.ray) {
      ray=p.ray;
      const double* entrance=p.ins<2?radial_in+(entry_surface*nz+j)*k:axial_in+r*k;
      std::copy(entrance,entrance+k,state.begin());
    }
    for(int c=0;c<k;++c) {
      const double sigma=total[(r*nz+j)*k+c];
      double t,b,d;coeff(l,sigma,t,b,d);
      const double incoming=state[c],value=b*incoming+d*source[c],out=t*incoming+b*source[c];
      fields[p.cell*9*k+c]+=p.weight*value;
      fields[(p.cell*9+1+p.ins)*k+c]+=p.weight*incoming;
      fields[(p.cell*9+5+p.outs)*k+c]+=p.weight*out;state[c]=out;
      const double defect=out-incoming+sigma*value-l*source[c];
      const double supply=std::abs(incoming)+l*std::abs(source[c]),err=ratio(defect,supply);
      double* m=metrics+c*nm;m[0]=std::min(m[0],std::min(incoming,out));m[1]=std::min(m[1],value);
      if(err>m[2]) {
        m[2]=err;m[3]=index;m[4]=incoming;m[5]=out;m[6]=value;m[7]=defect;
        m[8]=supply;m[9]=l;m[10]=sigma;m[11]=source[c];
      }
    }
  }
  for(int i=0;i<nr;++i)for(int j=0;j<nz;++j)for(int c=0;c<k;++c) {
    int cell=i*nz+j,r=regions[i];double* m=metrics+c*nm;
    double fin=0.,fout=0.,bi=0.,bo=0.,abs_fin=0.,abs_bi=0.;
    for(int side=0;side<4;++side) {
      const double in=fields[(cell*9+1+side)*k+c],out=fields[(cell*9+5+side)*k+c];
      fin+=in;fout+=out;abs_fin+=std::abs(in);
      if((side==0&&i==0)||(side==1&&i==nr-1)||(side==2&&j==0)||(side==3&&j==nz-1)) {
        bi+=in;bo+=out;abs_bi+=std::abs(in);
      }
    }
    const double born=g.w[i]*(g.z[j+1]-g.z[j])*q[(r*nz+j)*k+c];
    const double collision=total[(r*nz+j)*k+c]*fields[cell*9*k+c];
    const double defect=born+fin-fout-collision,supply=std::abs(born)+abs_fin,err=ratio(defect,supply);
    if(err>m[12]) {
      m[12]=err;m[13]=cell;m[14]=born;m[15]=fin;m[16]=fout;m[17]=collision;
      m[18]=defect;m[19]=supply;
    }
    m[20]+=born;m[21]+=bi;m[22]+=bo;m[23]+=collision;
    m[25]+=std::abs(born)+abs_bi;
  }
  for(int c=0;c<k;++c) {
    double* m=metrics+c*nm;m[24]=m[20]+m[21]-m[22]-m[23];
    for(int i=0;i<nr;++i)for(int j=0;j<nz;++j) {
      int a=i*nz+j;
      if(i+1<nr) {
        int b=(i+1)*nz+j;
        double out=orientation==1?fields[(a*9+6)*k+c]:fields[(b*9+5)*k+c];
        double in=orientation==1?fields[(b*9+1)*k+c]:fields[(a*9+2)*k+c];
        m[26]=std::max(m[26],std::abs(out-in));
      }
      if(j+1<nz) {
        int b=a+1;
        double out=mu>0?fields[(a*9+8)*k+c]:fields[(b*9+7)*k+c];
        double in=mu>0?fields[(b*9+3)*k+c]:fields[(a*9+4)*k+c];
        m[26]=std::max(m[26],std::abs(out-in));
      }
    }
  }
  for(int i=0;i<nc*9*k;++i)if(!std::isfinite(fields[i]))return -5;
  for(int i=0;i<k*nm;++i)if(!std::isfinite(metrics[i]))return -6;
  return 0;
}
}

// total is (8,nz,k), q is (8*nz,k); each column is a separate group action.
// This fixed-source component has no eigenproblem, white closure or admission.
extern "C" int layered_transport_multigroup(int nr,int nz,int k,const double* widths,
  const int* regions,const double* total,int entry_surface,double H,double mu,
  int orientation,int order,const double* gn,const double* gw,const double* q,
  const double* radial_in,const double* axial_in,double* geometric,
  double* fields,double* metrics) {
  return multigroup_core(nr,nz,k,widths,regions,total,entry_surface,H,mu,
    orientation,order,gn,gw,q,radial_in,axial_in,geometric,fields,metrics);
}
