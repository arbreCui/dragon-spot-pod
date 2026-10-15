// Standalone preflight only. No production headers, transport, or native tables.
// The arithmetic and tie rules follow native_oblique_track_geometry.py.
#include <algorithm>
#include <cmath>
#include <limits>
#include <vector>

extern "C" int geometry_count(int nt, int stride, const int* counts,
    const double* planar, double zmu, double H, int nz, double mu,
    int orientation, int order, const double* gn, const double* gw,
    double* metrics, double* raw) {
  if (nz < 1 || nz > 4 || (orientation != 1 && orientation != -1) || mu == 0) return -1;
  // metrics: intervals, chords, pieces, min_length, min_weight,
  // volume_error, incoming_error, outgoing_error, represented_width_error,
  // worst_kind (0 volume / 1 incoming / 2 outgoing), cell, side, actual,
  // expected, zero_piece_count, rounded_endpoint_nodes, min_break_width.
  constexpr int nm = 17;
  for (int tr=0; tr<nt; ++tr) {
    int nr=counts[tr], nc=nr*nz;
    if (nr<1 || nr>15) return -2;
    double* out=metrics+tr*nm; double* r=raw+tr*15*nz*9;
    std::fill(out,out+nm,0.); std::fill(r,r+15*nz*9,0.);
    std::vector<double> w(nr),x(nr+1,0.),se(nr+1),z(nz+1),br;
    for(int i=0;i<nr;++i) {w[i]=planar[tr*stride+i]*zmu; x[i+1]=x[i]+w[i];}
    double S=x.back();
    for(int i=0;i<=nr;++i) se[i]=orientation==1?x[i]:S-x[nr-i];
    for(int j=0;j<=nz;++j) z[j]=j==nz?H:j*(H/nz);
    for(double zv:z) for(double sv:se) br.push_back(zv-mu*sv);
    std::sort(br.begin(),br.end());br.erase(std::unique(br.begin(),br.end()),br.end());
    out[0]=br.size()-1;out[1]=out[0]*order;
    out[3]=out[4]=out[16]=std::numeric_limits<double>::infinity();
    for(size_t b=0;b+1<br.size();++b) {
      double delta=br[b+1]-br[b];out[16]=std::min(out[16],delta);
      for(int node=0;node<order;++node) {
        double u=(br[b]+br[b+1])/2+delta*gn[node]/2;
        double weight=delta*gw[node]/2;out[4]=std::min(out[4],weight);
        if (!(u>br[b] && u<br[b+1])) out[15]+=1;
        double start,stop;int ins,outs;
        if(mu>0) {start=std::max(0.,-u/mu);stop=std::min(S,(H-u)/mu);
          ins=start==0?(orientation==1?0:1):2;outs=stop==S?(orientation==1?1:0):3;
        } else {start=std::max(0.,(H-u)/mu);stop=std::min(S,-u/mu);
          ins=start==0?(orientation==1?0:1):3;outs=stop==S?(orientation==1?1:0):2;}
        if(!(stop>start)) return -3;
        std::vector<std::pair<double,int>> cut{{start,ins}};
        for(int i=1;i<nr;++i) if(start<se[i] && se[i]<stop) cut.emplace_back(se[i],orientation==1?1:0);
        for(int j=1;j<nz;++j) {double s=(z[j]-u)/mu;
          if(start<s && s<stop) cut.emplace_back(s,mu>0?3:2);}
        cut.emplace_back(stop,outs);
        // Stable ties agree with Python's points.sort() including side number.
        std::sort(cut.begin(),cut.end());int side_in=ins;
        for(size_t k=0;k+1<cut.size();++k) {
          double a=cut[k].first,b1=cut[k+1].first,len=b1-a;
          if(len==0) {out[14]+=1;continue;}
          double mid=(a+b1)/2,xp=orientation==1?mid:S-mid,zp=u+mu*mid;
          int i=std::upper_bound(x.begin(),x.end(),xp)-x.begin()-1;
          int j=std::upper_bound(z.begin(),z.end(),zp)-z.begin()-1;
          if(i<0 || i>=nr || j<0 || j>=nz || len<0) return -4;
          int cell=i*nz+j,side_out=cut[k+1].second;
          r[cell*9]+=weight*len;r[cell*9+1+side_in]+=weight;r[cell*9+5+side_out]+=weight;
          out[2]+=1;out[3]=std::min(out[3],len);side_in=side_out^1;
        }
      }
    }
    double worst=-1.;
    for(int i=0;i<nr;++i) {
      out[8]=std::max(out[8],std::abs((x[i+1]-x[i])-w[i])/w[i]);
      for(int j=0;j<nz;++j) {
        int c=i*nz+j;double dz=z[j+1]-z[j];
        for(int k=0;k<9;++k) {
          int kind=k==0?0:(k<5?1:2),side=k==0?-1:(k-1)%4;
          double expected;
          if(k==0) expected=w[i]*dz;
          else {
            bool incoming=(side==(orientation==1?0:1) || side==(mu>0?2:3));
            bool active=(kind==1?incoming:!incoming);
            expected=active?(side<2?dz:std::abs(mu)*w[i]):0.;
          }
          double actual=r[c*9+k];
          double error=expected>0?std::abs(actual-expected)/expected:(actual==0?0:std::numeric_limits<double>::infinity());
          out[5+kind]=std::max(out[5+kind],error);
          if(error>worst) {worst=error;out[9]=kind;out[10]=c;out[11]=side;out[12]=actual;out[13]=expected;}
        }
      }
    }
    for(int i=0;i<nm;++i) if(!std::isfinite(out[i])) return -5;
  }
  return 0;
}
