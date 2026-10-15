// Standalone exact-characteristic experiment. No production dependencies.
#include <algorithm>
#include <array>
#include <cmath>
#include <limits>
#include <vector>

namespace {
constexpr int K=16, U=14, M=48;
struct Piece { int ray,cell,ins,outs; double a,b,weight; };
struct Geo {
  int nr,nz; double S,H,mu; int orient;
  std::vector<double> w,x,z,br; std::vector<Piece> pieces;
  std::vector<double> raw; int chords=0;
};
double ratio(double a,double b) {return b>0?std::abs(a)/b:(a==0?0:std::numeric_limits<double>::infinity());}
void coeff(double l,double s,double& t,double& b,double& d) {
  double tau=l*s;t=std::exp(-tau);b=s==0?l:-std::expm1(-tau)/s;
  if(tau<=.5) {
    // Same converged series as the independently tested Python primitive.
    double fact=1.;double c[19];for(int k=1;k<=20;++k) {fact*=k;if(k>=2)c[k-2]=(k%2==0?1.:-1.)/fact;}
    double v=c[18];for(int k=17;k>=0;--k)v=v*tau+c[k];d=l*l*v;
  } else d=(l-b)/s;
}
int make_geo(const double* w,int nr,double H,int nz,double mu,int o,int order,const double* gn,const double* gw,Geo& g) {
  g.nr=nr;g.nz=nz;g.H=H;g.mu=mu;g.orient=o;g.w.assign(w,w+nr);g.x.assign(nr+1,0.);g.z.resize(nz+1);
  for(int i=0;i<nr;++i)g.x[i+1]=g.x[i]+w[i];g.S=g.x.back();
  std::vector<double> se(nr+1);for(int i=0;i<=nr;++i)se[i]=o==1?g.x[i]:g.S-g.x[nr-i];
  for(int j=0;j<=nz;++j)g.z[j]=j==nz?H:j*(H/nz);
  for(double z:g.z)for(double s:se)g.br.push_back(z-mu*s);
  std::sort(g.br.begin(),g.br.end());g.br.erase(std::unique(g.br.begin(),g.br.end()),g.br.end());
  g.raw.assign(nr*nz*9,0.);
  for(size_t k=0;k+1<g.br.size();++k)for(int node=0;node<order;++node) {
    double delta=g.br[k+1]-g.br[k],u=(g.br[k]+g.br[k+1])/2+delta*gn[node]/2,weight=delta*gw[node]/2;
    if(!(u>g.br[k] && u<g.br[k+1]))return -11;
    double start,stop;int ins,outs;
    if(mu>0){start=std::max(0.,-u/mu);stop=std::min(g.S,(H-u)/mu);ins=start==0?(o==1?0:1):2;outs=stop==g.S?(o==1?1:0):3;}
    else {start=std::max(0.,(H-u)/mu);stop=std::min(g.S,-u/mu);ins=start==0?(o==1?0:1):3;outs=stop==g.S?(o==1?1:0):2;}
    if(!(stop>start))return -12;
    std::vector<std::pair<double,int>> cut{{start,ins}};
    for(int i=1;i<nr;++i)if(start<se[i] && se[i]<stop)cut.emplace_back(se[i],o==1?1:0);
    for(int j=1;j<nz;++j){double s=(g.z[j]-u)/mu;if(start<s && s<stop)cut.emplace_back(s,mu>0?3:2);}
    cut.emplace_back(stop,outs);std::sort(cut.begin(),cut.end());int side=ins;
    for(size_t v=0;v+1<cut.size();++v) {
      double a=cut[v].first,b=cut[v+1].first;if(!(b>a))return -13;
      double mid=(a+b)/2,xp=o==1?mid:g.S-mid,zp=u+mu*mid;
      int i=std::upper_bound(g.x.begin(),g.x.end(),xp)-g.x.begin()-1,j=std::upper_bound(g.z.begin(),g.z.end(),zp)-g.z.begin()-1;
      if(i<0 || i>=nr || j<0 || j>=nz)return -14;int c=i*nz+j,out=cut[v+1].second;
      g.pieces.push_back({g.chords,c,side,out,a,b,weight});g.raw[c*9]+=weight*(b-a);g.raw[c*9+1+side]+=weight;g.raw[c*9+5+out]+=weight;side=out^1;
    }
    ++g.chords;
  }
  return 0;
}
double partial_b(double l,double sigma) {return sigma==0?l:-std::expm1(-sigma*l)/sigma;}
}

// refs: (group, track, original physical segment padded to 15, 14 columns).
// metrics: (track, group, 16 columns, 48 raw values); regional: (track,group,8,nz,14).
extern "C" int streaming_transport(int nt,int ng,const int* counts,const double* widths,
  const int* regions,const double* totals,const double* ref_in,const double* ref_out,const double* ref_int,
  double H,int nz,double mu,int orient,int order,const double* gn,const double* gw,
  double* geometry_receipt,double* metrics,double* regional,double* debug_fields) {
  if(nt<1 || ng<1 || nz<1 || nz>4 || mu==0 || (orient!=1 && orient!=-1))return -1;
  for(int tr=0;tr<nt;++tr) {
    int nr=counts[tr],nc=nr*nz;if(nr<1 || nr>15)return -2;
    Geo g;int rc=make_geo(widths+tr*15,nr,H,nz,mu,orient,order,gn,gw,g);if(rc)return rc;
    double* gm=geometry_receipt+tr*6;gm[0]=g.br.size()-1;gm[1]=g.chords;gm[2]=g.pieces.size();gm[3]=0.;gm[4]=std::numeric_limits<double>::infinity();gm[5]=0.;
    for(const auto& p:g.pieces)gm[4]=std::min(gm[4],p.b-p.a);
    for(int i=0;i<nr;++i)for(int j=0;j<nz;++j)for(int k=0;k<9;++k) {
      double expected=0.,dz=g.z[j+1]-g.z[j];int side=(k-1)%4;
      if(k==0)expected=g.w[i]*dz;
      else {bool incoming=side==(orient==1?0:1)||side==(mu>0?2:3);bool active=k<5?incoming:!incoming;
        if(active)expected=side<2?dz:std::abs(mu)*g.w[i];}
      gm[3]=std::max(gm[3],ratio(g.raw[(i*nz+j)*9+k]-expected,expected));
      gm[5]=std::max(gm[5],ratio((g.x[i+1]-g.x[i])-g.w[i],g.w[i]));
    }
    for(int group=0;group<ng;++group) {
      const double* sig=totals+group*8;const int* reg=regions+tr*15;
      size_t off=(size_t(group)*nt+tr)*15*U;
      const double* ri=ref_in+off;const double* ro=ref_out+off;const double* rv=ref_int+off;
      double* met=metrics+(size_t(tr)*ng+group)*K*M;
      double* regional_row=regional+(size_t(tr)*ng+group)*8*nz*U;
      std::fill(met,met+K*M,0.);std::fill(regional_row,regional_row+8*nz*U,0.);
      std::vector<double> f(nc*9*K,0.),source(nr*K,0.);std::array<double,K> state{},scale{};
      double alpha[2][U];for(int c=0;c<U;++c){alpha[0][c]=c<8?(c+1.)/8:(c-7.)/6;alpha[1][c]=c<8?sig[c]:1.;}
      for(int c=0;c<K;++c){met[c*M]=met[c*M+1]=std::numeric_limits<double>::infinity();met[c*M+2]=met[c*M+12]=-1.;}
      for(int i=0;i<nr;++i) {
        if(reg[i]<0 || reg[i]>=8 || sig[reg[i]]<0)return -3;
        source[i*K+reg[i]]=1.;source[i*K+14]=(reg[i]+1.)/8;source[i*K+15]=sig[reg[i]];
        for(int c=0;c<U;++c)scale[c]=std::max(scale[c],std::max(ri[i*U+c],ro[i*U+c]));
        double mixed_in=0,mixed_out=0;for(int c=0;c<U;++c){mixed_in+=ri[i*U+c]*alpha[0][c];mixed_out+=ro[i*U+c]*alpha[0][c];}
        scale[14]=std::max(scale[14],std::max(mixed_in,mixed_out));
      }
      scale[15]=1.;for(int c=0;c<K;++c)met[c*M+27]=scale[c];
      int ray=-1;
      for(size_t index=0;index<g.pieces.size();++index) {
        const auto& p=g.pieces[index];int i=p.cell/nz,r=reg[i];double sigma=sig[r],l=p.b-p.a;
        double t,b,d;coeff(l,sigma,t,b,d);
        double start=orient==1?g.x[i]:g.S-g.x[i+1],a=p.a-start,e=p.b-start;
        if(a<0 || e<0)return -15;
        double ta=std::exp(-sigma*a),ba=partial_b(a,sigma),te=std::exp(-sigma*e),be=partial_b(e,sigma);
        std::array<double,K> expect_in{},expect_out{};
        for(int c=0;c<U;++c){expect_in[c]=ta*ri[i*U+c]+ba*(c==r);expect_out[c]=te*ri[i*U+c]+be*(c==r);}
        for(int c=0;c<U;++c){expect_in[14]+=alpha[0][c]*expect_in[c];expect_out[14]+=alpha[0][c]*expect_out[c];}
        expect_in[15]=expect_out[15]=1.;
        if(ray!=p.ray){ray=p.ray;state=expect_in;}
        double* integral=&f[p.cell*9*K];double* facein=integral+(1+p.ins)*K;double* faceout=integral+(5+p.outs)*K;
        const double* q=&source[i*K];
        for(int c=0;c<K;++c) {
          double incoming=state[c],value=b*incoming+d*q[c],out=t*incoming+b*q[c];
          integral[c]+=p.weight*value;facein[c]+=p.weight*incoming;faceout[c]+=p.weight*out;state[c]=out;
          double defect=out-incoming+sigma*value-l*q[c],supply=incoming+l*q[c],err=ratio(defect,supply);double* m=met+c*M;
          m[0]=std::min(m[0],std::min(incoming,out));m[1]=std::min(m[1],value);
          if(err>m[2]){m[2]=err;m[3]=index;m[4]=incoming;m[5]=out;m[6]=value;m[7]=defect;m[8]=supply;m[9]=l;m[10]=sigma;m[11]=q[c];}
          double errin=std::abs(incoming-expect_in[c]),errout=std::abs(out-expect_out[c]);
          if(std::max(errin,errout)>m[26]) {bool end=errout>errin;m[26]=end?errout:errin;m[36]=index;m[37]=end?1:0;m[38]=end?out:incoming;m[39]=end?expect_out[c]:expect_in[c];}
        }
      }
      for(int i=0;i<nr;++i)for(int j=0;j<nz;++j) {
        int cell=i*nz+j,r=reg[i];double dz=g.z[j+1]-g.z[j],area=g.w[i]*dz;
        for(int c=0;c<K;++c) {
          double* m=met+c*M;double value=f[cell*9*K+c],fin=0,fout=0,boundary_in=0,boundary_out=0;
          for(int side=0;side<4;++side) {
            double in=f[(cell*9+1+side)*K+c],out=f[(cell*9+5+side)*K+c];fin+=in;fout+=out;
            if((side==0&&i==0)||(side==1&&i==nr-1)||(side==2&&j==0)||(side==3&&j==nz-1)){boundary_in+=in;boundary_out+=out;}
            double expected=0;
            if(side==(orient==1?1:0)) {
              if(c<U)expected=ro[i*U+c]*dz;
              else if(c==14){for(int u=0;u<U;++u)expected+=alpha[0][u]*ro[i*U+u]*dz;}
              else expected=dz;
            } else if(side==(mu>0?3:2)) {
              if(c<U)expected=std::abs(mu)*rv[i*U+c];
              else if(c==14){for(int u=0;u<U;++u)expected+=alpha[0][u]*std::abs(mu)*rv[i*U+u];}
              else expected=std::abs(mu)*g.w[i];
            }
            double error=std::abs(out-expected);m[31]=std::max(m[31],expected);
            if(error>m[30]){m[30]=error;m[43]=cell*4+side;m[44]=out;m[45]=expected;}
          }
          double birth=area*source[i*K+c],collision=sig[r]*value,defect=birth+fin-fout-collision,supply=birth+fin,error=ratio(defect,supply);
          if(error>m[12]){m[12]=error;m[13]=cell;m[14]=birth;m[15]=fin;m[16]=fout;m[17]=collision;m[18]=defect;m[19]=supply;}
          m[20]+=birth;m[21]+=boundary_in;m[22]+=boundary_out;m[23]+=collision;m[32]+=value;
          if(i==(orient==1?nr-1:0))m[33]+=f[(cell*9+5+(orient==1?1:0))*K+c];
          double expected=0;if(c<U)expected=rv[i*U+c]*dz;
          else if(c==14){for(int u=0;u<U;++u)expected+=alpha[0][u]*rv[i*U+u]*dz;}else expected=area;
          error=std::abs(value-expected);m[29]=std::max(m[29],expected);
          if(error>m[28]){m[28]=error;m[40]=cell;m[41]=value;m[42]=expected;}
          m[34]+=expected;
          if(c<U)regional_row[(r*nz+j)*U+c]+=value;
        }
      }
      for(int c=0;c<K;++c){double* m=met+c*M;m[24]=m[20]+m[21]-m[22]-m[23];m[25]=m[20]+m[21];
        int end=orient==1?nr-1:0;
        if(c<U)m[35]=ro[end*U+c]*H;else if(c==14){for(int u=0;u<U;++u)m[35]+=alpha[0][u]*ro[end*U+u]*H;}else m[35]=H;}
      // Independently swept controls versus the assembled full input basis.
      for(int ctrl=0;ctrl<2;++ctrl)for(int kind=0;kind<9;++kind){double error=0,amplitude=0;
        for(int cell=0;cell<nc;++cell){const double* v=&f[(cell*9+kind)*K];double assembled=0;
          for(int u=0;u<U;++u)assembled+=v[u]*alpha[ctrl][u];error=std::max(error,std::abs(assembled-v[U+ctrl]));amplitude=std::max(amplitude,std::abs(v[U+ctrl]));}
        met[(U+ctrl)*M+46]=std::max(met[(U+ctrl)*M+46],ratio(error,amplitude));}
      // Shared faces must be bitwise identical before any regional aggregation.
      double shared=0.;for(int i=0;i<nr;++i)for(int j=0;j<nz;++j)for(int c=0;c<K;++c){
        int cell=i*nz+j;
        if(i+1<nr){int left=cell,right=(i+1)*nz+j;double a=orient==1?f[(left*9+6)*K+c]:f[(right*9+5)*K+c];double b=orient==1?f[(right*9+1)*K+c]:f[(left*9+2)*K+c];shared=std::max(shared,std::abs(a-b));}
        if(j+1<nz){int lower=cell,upper=cell+1;double a=mu>0?f[(lower*9+8)*K+c]:f[(upper*9+7)*K+c];double b=mu>0?f[(upper*9+3)*K+c]:f[(lower*9+4)*K+c];shared=std::max(shared,std::abs(a-b));}}
      for(int c=0;c<K;++c)met[c*M+47]=shared;
      for(int c=0;c<K*M;++c)if(!std::isfinite(met[c]))return -16;
      if(debug_fields){double* to=debug_fields+(size_t(tr)*ng+group)*15*nz*9*K;std::fill(to,to+15*nz*9*K,0.);std::copy(f.begin(),f.end(),to);}
    }
  }
  return 0;
}
