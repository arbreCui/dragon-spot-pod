// Geometry and primitive copied verbatim from the sealed zero-gradient kernel.
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

