// Standalone layered-source transport; ordinary doubles, no production link.
#include "native_oblique_geometry_core.hpp"
#include "native_layered_geometry.hpp"

// q:(8*nz,k), radial_in:(6*nz,k), axial_in:(8,k).
// The optional matched reference is used ONLY when matched_mode is explicitly
// selected for regression. In physical mode it is never dereferenced.
extern "C" int layered_transport(int nr,int nz,int k,const double* widths,
  const int* regions,const double* total,int entry_surface,double H,double mu,
  int orientation,int order,const double* gn,const double* gw,const double* q,
  const double* radial_in,const double* axial_in,int matched_mode,
  const double* matched_reference,double* geometric,double* fields,double* metrics) {
  constexpr int nm=27;
  if(nr<1||nr>15||nz<1||nz>64||k<1||k>2048||!(H>0)||!std::isfinite(H)||
     !(std::abs(mu)>0&&std::abs(mu)<1)||order<2||order>128||
     (orientation!=1&&orientation!=-1)||entry_surface<0||entry_surface>=6||
     (matched_mode!=0&&matched_mode!=1))return -1;
  for(int i=0;i<nr;++i)if(!(widths[i]>0)||!std::isfinite(widths[i])||regions[i]<0||regions[i]>=8)return -2;
  for(int r=0;r<8;++r)if(total[r]<0||!std::isfinite(total[r]))return -3;
  // Single-entry geometry cache; numerical sources and totals are never cached.
  // The caller is deliberately single-threaded. Every geometry-defining binary64
  // input, including the offset rule, participates in this exact key.
  static std::vector<double> last_key;
  static Geo cached_geometry;
  static std::vector<double> cached_lengths;
  std::vector<double> key{double(nr),double(nz),H,mu,double(orientation),double(order),double(matched_mode)};
  key.insert(key.end(),widths,widths+nr);key.insert(key.end(),gn,gn+order);key.insert(key.end(),gw,gw+order);
  if(key!=last_key) {
    Geo next;std::vector<double> next_lengths;
    int rc=matched_mode?make_geo(widths,nr,H,nz,mu,orientation,order,gn,gw,next):
      make_layered_geo(widths,nr,H,nz,mu,orientation,order,gn,gw,next,next_lengths);
    if(rc)return rc;
    cached_geometry=std::move(next);cached_lengths=std::move(next_lengths);last_key=std::move(key);
  }
  const Geo& g=cached_geometry;const std::vector<double>& lengths=cached_lengths;
  const int nc=nr*nz;
  std::fill(fields,fields+nc*9*k,0.);std::fill(metrics,metrics+k*nm,0.);
  geometric[0]=g.br.size()-1;geometric[1]=g.chords;geometric[2]=g.pieces.size();
  geometric[3]=0.;geometric[4]=std::numeric_limits<double>::infinity();geometric[5]=0.;
  for(size_t i=0;i<g.pieces.size();++i)geometric[4]=std::min(geometric[4],matched_mode?g.pieces[i].b-g.pieces[i].a:lengths[i]);
  for(int i=0;i<nr;++i)for(int j=0;j<nz;++j) {
    const double dz=g.z[j+1]-g.z[j];
    geometric[5]=std::max(geometric[5],ratio(g.x[i+1]-g.x[i]-g.w[i],g.w[i]));
    for(int f=0;f<9;++f) {
      double expected=0.;
      if(f==0)expected=g.w[i]*dz;
      else {int side=(f-1)%4;bool incoming=side==(orientation==1?0:1)||side==(mu>0?2:3);
        if((f<5&&incoming)||(f>=5&&!incoming))expected=side<2?dz:std::abs(mu)*g.w[i];}
      geometric[3]=std::max(geometric[3],ratio(g.raw[(i*nz+j)*9+f]-expected,expected));
    }
  }
  for(int c=0;c<k;++c) {
    double* m=metrics+c*nm;m[0]=m[1]=std::numeric_limits<double>::infinity();m[2]=m[12]=-1.;
  }
  std::vector<double> state(k);int ray=-1;
  for(size_t index=0;index<g.pieces.size();++index) {
    const auto& p=g.pieces[index];int i=p.cell/nz,j=p.cell%nz,r=regions[i];
    const double sigma=total[r],l=matched_mode?p.b-p.a:lengths[index];const double* source=q+(r*nz+j)*k;
    if(ray!=p.ray) {
      ray=p.ray;
      if(matched_mode) {
        const double start=orientation==1?g.x[i]:g.S-g.x[i+1],s=p.a-start;
        if(s<0||!matched_reference)return -4;
        for(int c=0;c<k;++c)state[c]=std::exp(-sigma*s)*matched_reference[i*k+c]+partial_b(s,sigma)*source[c];
      } else {
        const double* entrance=p.ins<2?radial_in+(entry_surface*nz+j)*k:axial_in+r*k;
        std::copy(entrance,entrance+k,state.begin());
      }
    }
    double t,b,d;coeff(l,sigma,t,b,d);
    for(int c=0;c<k;++c) {
      const double incoming=state[c],value=b*incoming+d*source[c],out=t*incoming+b*source[c];
      fields[p.cell*9*k+c]+=p.weight*value;
      fields[(p.cell*9+1+p.ins)*k+c]+=p.weight*incoming;
      fields[(p.cell*9+5+p.outs)*k+c]+=p.weight*out;state[c]=out;
      const double defect=out-incoming+sigma*value-l*source[c],supply=incoming+l*source[c],err=ratio(defect,supply);
      double* m=metrics+c*nm;m[0]=std::min(m[0],std::min(incoming,out));m[1]=std::min(m[1],value);
      if(err>m[2]){m[2]=err;m[3]=index;m[4]=incoming;m[5]=out;m[6]=value;m[7]=defect;m[8]=supply;m[9]=l;m[10]=sigma;m[11]=source[c];}
    }
  }
  for(int i=0;i<nr;++i)for(int j=0;j<nz;++j)for(int c=0;c<k;++c) {
    int cell=i*nz+j,r=regions[i];double* m=metrics+c*nm;
    double fin=0.,fout=0.,bi=0.,bo=0.;
    for(int side=0;side<4;++side) {
      const double in=fields[(cell*9+1+side)*k+c],out=fields[(cell*9+5+side)*k+c];fin+=in;fout+=out;
      if((side==0&&i==0)||(side==1&&i==nr-1)||(side==2&&j==0)||(side==3&&j==nz-1)){bi+=in;bo+=out;}
    }
    const double born=g.w[i]*(g.z[j+1]-g.z[j])*q[(r*nz+j)*k+c],collision=total[r]*fields[cell*9*k+c];
    const double defect=born+fin-fout-collision,supply=born+fin,err=ratio(defect,supply);
    if(err>m[12]){m[12]=err;m[13]=cell;m[14]=born;m[15]=fin;m[16]=fout;m[17]=collision;m[18]=defect;m[19]=supply;}
    m[20]+=born;m[21]+=bi;m[22]+=bo;m[23]+=collision;
  }
  for(int c=0;c<k;++c) {double* m=metrics+c*nm;m[24]=m[20]+m[21]-m[22]-m[23];m[25]=m[20]+m[21];
    for(int i=0;i<nr;++i)for(int j=0;j<nz;++j) {
      int a=i*nz+j;
      if(i+1<nr){int b=(i+1)*nz+j;
        double out=orientation==1?fields[(a*9+6)*k+c]:fields[(b*9+5)*k+c];
        double in=orientation==1?fields[(b*9+1)*k+c]:fields[(a*9+2)*k+c];m[26]=std::max(m[26],std::abs(out-in));}
      if(j+1<nz){int b=a+1;
        double out=mu>0?fields[(a*9+8)*k+c]:fields[(b*9+7)*k+c];
        double in=mu>0?fields[(b*9+3)*k+c]:fields[(a*9+4)*k+c];m[26]=std::max(m[26],std::abs(out-in));}
    }
  }
  for(int i=0;i<nc*9*k;++i)if(!std::isfinite(fields[i]))return -5;
  for(int i=0;i<k*nm;++i)if(!std::isfinite(metrics[i]))return -6;
  return 0;
}
