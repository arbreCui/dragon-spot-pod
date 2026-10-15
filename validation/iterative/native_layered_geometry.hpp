// Physical geometry uses 113-bit intersections; stored transport values remain
// binary64. The sealed matched-inflow regression retains its original geometry.
#include <boost/multiprecision/cpp_bin_float.hpp>
namespace {
using Coordinate=boost::multiprecision::cpp_bin_float_quad;
int make_layered_geo(const double* widths,int nr,double H,int nz,double mu,int o,
  int order,const double* gn,const double* gw,Geo& g,std::vector<double>& lengths) {
  using R=Coordinate;
  g.nr=nr;g.nz=nz;g.H=H;g.mu=mu;g.orient=o;g.w.assign(widths,widths+nr);
  std::vector<R> x(nr+1),z(nz+1),se(nr+1),breaks;
  for(int i=0;i<nr;++i)x[i+1]=x[i]+R(widths[i]);
  R S=x.back(),M=R(mu),height=R(H);
  g.S=static_cast<double>(S);g.x.resize(nr+1);g.z.resize(nz+1);
  for(int i=0;i<=nr;++i){g.x[i]=static_cast<double>(x[i]);se[i]=o==1?x[i]:S-x[nr-i];}
  for(int j=0;j<=nz;++j){z[j]=height*j/nz;g.z[j]=static_cast<double>(z[j]);}
  for(const R& zz:z)for(const R& ss:se)breaks.push_back(zz-M*ss);
  std::sort(breaks.begin(),breaks.end());breaks.erase(std::unique(breaks.begin(),breaks.end()),breaks.end());
  for(const R& b:breaks)g.br.push_back(static_cast<double>(b));
  g.raw.assign(nr*nz*9,0.);
  for(size_t k=0;k+1<breaks.size();++k)for(int node=0;node<order;++node){
    R delta=breaks[k+1]-breaks[k],u=(breaks[k]+breaks[k+1])/2+delta*R(gn[node])/2;
    double weight=static_cast<double>(delta*R(gw[node])/2);
    if(!(u>breaks[k]&&u<breaks[k+1])||!(weight>0))return -21;
    R start,stop;int ins,outs;
    if(mu>0){start=std::max(R(0),R(-u/M));stop=std::min(S,R((height-u)/M));ins=start==0?(o==1?0:1):2;outs=stop==S?(o==1?1:0):3;}
    else{start=std::max(R(0),R((height-u)/M));stop=std::min(S,R(-u/M));ins=start==0?(o==1?0:1):3;outs=stop==S?(o==1?1:0):2;}
    if(!(stop>start))return -22;
    std::vector<std::pair<R,int>> cuts{{start,ins}};
    for(int i=1;i<nr;++i)if(start<se[i]&&se[i]<stop)cuts.emplace_back(se[i],o==1?1:0);
    for(int j=1;j<nz;++j){R s=(z[j]-u)/M;if(start<s&&s<stop)cuts.emplace_back(s,mu>0?3:2);}
    cuts.emplace_back(stop,outs);std::sort(cuts.begin(),cuts.end());int side=ins;
    for(size_t v=0;v+1<cuts.size();++v){
      R a=cuts[v].first,b=cuts[v+1].first;if(!(b>a))return -23;
      R mid=(a+b)/2,xp=o==1?mid:S-mid,zp=u+M*mid;
      int i=std::upper_bound(x.begin(),x.end(),xp)-x.begin()-1,j=std::upper_bound(z.begin(),z.end(),zp)-z.begin()-1;
      if(i<0||i>=nr||j<0||j>=nz)return -24;
      int c=i*nz+j,out=cuts[v+1].second;double length=static_cast<double>(b-a);
      if(!(length>0))return -25;
      g.pieces.push_back({g.chords,c,side,out,static_cast<double>(a),static_cast<double>(b),weight});lengths.push_back(length);
      g.raw[c*9]+=weight*length;g.raw[c*9+1+side]+=weight;g.raw[c*9+5+out]+=weight;side=out^1;
    }
    ++g.chords;
  }
  return 0;
}
}
