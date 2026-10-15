// Radial white inflow to boundary currents on the unchanged physical geometry.
// Keep the three saved transport exports available for direct regression.
#include "native_layered_multigroup.cpp"

namespace {
int white_transfer_core(int nr,int nz,int k,const double* widths,
  const int* regions,const double* total,int entry_surface,int exit_surface,
  double H,double mu,int orientation,int order,const double* gn,const double* gw,
  double* geometric,double* transfer,double* leakage,double* incoming) {
  if(nr<1||nr>15||nz<1||nz>64||k<1||k>370||!(H>0)||!std::isfinite(H)||
     !(std::abs(mu)>0&&std::abs(mu)<1)||order<2||order>128||
     (orientation!=1&&orientation!=-1)||entry_surface<0||entry_surface>=6||
     exit_surface<0||exit_surface>=6||entry_surface==exit_surface)return -1;
  if(!widths||!regions||!total||!gn||!gw||!geometric||!transfer||!leakage||!incoming)
    return -7;
  for(int i=0;i<nr;++i)
    if(!(widths[i]>0)||!std::isfinite(widths[i])||regions[i]<0||regions[i]>=8)
      return -2;
  for(int i=0;i<8*nz*k;++i)if(total[i]<0||!std::isfinite(total[i]))return -3;
  for(int i=0;i<order;++i)
    if(!(gn[i]>-1&&gn[i]<1)||!(gw[i]>0)||!std::isfinite(gw[i]))return -3;
  Geo g;std::vector<double> lengths;
  int rc=make_layered_geo(widths,nr,H,nz,mu,orientation,order,gn,gw,g,lengths);
  if(rc)return rc;
  const int nwhite=6*nz;
  std::fill(transfer,transfer+nwhite*nwhite*k,0.);
  std::fill(leakage,leakage+2*8*nwhite*k,0.);
  std::fill(incoming,incoming+nwhite,0.);
  geometric[0]=g.br.size()-1;geometric[1]=g.chords;geometric[2]=g.pieces.size();
  geometric[3]=geometric[4]=0.;geometric[5]=std::numeric_limits<double>::infinity();
  std::vector<double> optical(k);
  for(size_t first=0;first<g.pieces.size();) {
    size_t last=first+1;
    while(last<g.pieces.size()&&g.pieces[last].ray==g.pieces[first].ray)++last;
    const auto& entrance=g.pieces[first];const auto& out=g.pieces[last-1];
    for(size_t index=first;index<last;++index)
      geometric[5]=std::min(geometric[5],lengths[index]);
    if(entrance.ins>=2) { // Both axial entering faces are exactly vacuum.
      geometric[4]+=1.;first=last;continue;
    }
    if(entrance.ins!=(orientation==1?0:1))return -4;
    geometric[3]+=1.;int column=entry_surface*nz+entrance.cell%nz;
    // Independent geometric denominator: first-piece weights only, no fitting.
    incoming[column]+=entrance.weight;std::fill(optical.begin(),optical.end(),0.);
    for(size_t index=first;index<last;++index) {
      const auto& p=g.pieces[index];int r=regions[p.cell/nz],z=p.cell%nz;
      for(int c=0;c<k;++c)optical[c]+=total[(r*nz+z)*k+c]*lengths[index];
    }
    if(out.outs<2) {
      if(out.outs!=(orientation==1?1:0))return -4;
      int row=exit_surface*nz+out.cell%nz;
      for(int c=0;c<k;++c)
        transfer[(row*nwhite+column)*k+c]+=out.weight*std::exp(-optical[c]);
    } else {
      int side=out.outs-2,r=regions[out.cell/nz];
      for(int c=0;c<k;++c)
        leakage[((side*8+r)*nwhite+column)*k+c]+=out.weight*std::exp(-optical[c]);
    }
    first=last;
  }
  for(int i=0;i<nwhite*nwhite*k;++i)
    if(!std::isfinite(transfer[i])||transfer[i]<0)return -5;
  for(int i=0;i<2*8*nwhite*k;++i)
    if(!std::isfinite(leakage[i])||leakage[i]<0)return -5;
  for(int i=0;i<nwhite;++i)if(!std::isfinite(incoming[i])||incoming[i]<0)return -5;
  for(int i=0;i<6;++i)if(!std::isfinite(geometric[i]))return -6;
  return 0;
}
}

// Caller supplies the two actual track surfaces for THIS orientation: swap the
// original track ends when orientation=-1. Local sides0/1 are not surface IDs.
// transfer=(6*nz,6*nz,k), leakage=(2,8,6*nz,k), incoming=(6*nz), C order.
// Leakage side0 is the bottom, side1 the top. No angular weight or normalization.
extern "C" int layered_white_radial_transfer(int nr,int nz,int k,
  const double* widths,const int* regions,const double* total,
  int entry_surface,int exit_surface,double H,double mu,int orientation,int order,
  const double* gn,const double* gw,double* geometric,double* transfer,
  double* leakage,double* incoming) {
  return white_transfer_core(nr,nz,k,widths,regions,total,entry_surface,exit_surface,
    H,mu,orientation,order,gn,gw,geometric,transfer,leakage,incoming);
}
