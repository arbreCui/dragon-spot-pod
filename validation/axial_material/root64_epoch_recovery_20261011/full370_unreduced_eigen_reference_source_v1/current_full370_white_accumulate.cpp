// Complete actual group accumulation without an additional per-ray T array.
// Old exports/geometry/coefficients coexist byte-for-byte through this include.
#include "native_layered_white_transfer.cpp"

extern "C" int layered_white_accumulate370(int nr,int nz,int k,
  const double* widths,const int* regions,const double* total,
  int entry_surface,int exit_surface,double H,double mu,int orientation,
  int order,const double* gn,const double* gw,double angular_track_weight,
  double* geometric,double* transfer_sum,double* leakage_sum,double* incoming_sum) {
  if(nr<1||nr>15||nz!=48||k!=370||H!=150.||!std::isfinite(H)||
     !(std::abs(mu)>0&&std::abs(mu)<1)||order<2||order>128||
     (orientation!=1&&orientation!=-1)||entry_surface<0||entry_surface>=6||
     exit_surface<0||exit_surface>=6||entry_surface==exit_surface||
     !(angular_track_weight>0)||!std::isfinite(angular_track_weight))return -1;
  if(!widths||!regions||!total||!gn||!gw||!geometric||!transfer_sum||
     !leakage_sum||!incoming_sum)return -7;
  for(int i=0;i<nr;++i)
    if(!(widths[i]>0)||!std::isfinite(widths[i])||regions[i]<0||regions[i]>=8)return -2;
  for(int i=0;i<8*nz*k;++i)
    if(total[i]<0||!std::isfinite(total[i]))return -3;
  for(int i=0;i<order;++i)
    if(!(gn[i]>-1&&gn[i]<1)||!(gw[i]>0)||!std::isfinite(gw[i]))return -3;
  Geo g;std::vector<double> lengths;
  int rc=make_layered_geo(widths,nr,H,nz,mu,orientation,order,gn,gw,g,lengths);
  if(rc)return rc;
  const int nwhite=6*nz;
  // One ray touches only its own entrance face and exit face. These compact
  // buffers retain the ORIGINAL per-ray chord summation and apply the original
  // angular/track weight ONCE afterward, avoiding both a second full288^2*370
  // matrix and any change to the original floating summation association.
  std::vector<double> local_transfer(nz*nz*k,0.);
  std::vector<double> local_leakage(2*8*nz*k,0.);
  std::vector<double> local_incoming(nz,0.);
  geometric[0]=g.br.size()-1;geometric[1]=g.chords;geometric[2]=g.pieces.size();
  geometric[3]=geometric[4]=0.;geometric[5]=std::numeric_limits<double>::infinity();
  std::vector<double> optical(k);
  for(size_t first=0;first<g.pieces.size();) {
    size_t last=first+1;
    while(last<g.pieces.size()&&g.pieces[last].ray==g.pieces[first].ray)++last;
    const auto& entrance=g.pieces[first];const auto& out=g.pieces[last-1];
    for(size_t index=first;index<last;++index)
      geometric[5]=std::min(geometric[5],lengths[index]);
    if(entrance.ins>=2) { // Exactly vacuum on both axial entering faces.
      geometric[4]+=1.;first=last;continue;
    }
    if(entrance.ins!=(orientation==1?0:1))return -4;
    geometric[3]+=1.;int column=entrance.cell%nz;
    local_incoming[column]+=entrance.weight;
    std::fill(optical.begin(),optical.end(),0.);
    for(size_t index=first;index<last;++index) {
      const auto& p=g.pieces[index];int r=regions[p.cell/nz],z=p.cell%nz;
      for(int c=0;c<k;++c)optical[c]+=total[(r*nz+z)*k+c]*lengths[index];
    }
    if(out.outs<2) {
      if(out.outs!=(orientation==1?1:0))return -4;
      int row=out.cell%nz;
      for(int c=0;c<k;++c)
        local_transfer[(row*nz+column)*k+c]+=out.weight*std::exp(-optical[c]);
    } else {
      int side=out.outs-2,r=regions[out.cell/nz];
      for(int c=0;c<k;++c)
        local_leakage[((side*8+r)*nz+column)*k+c]+=out.weight*std::exp(-optical[c]);
    }
    first=last;
  }
  for(int j=0;j<nz;++j) {
    if(!std::isfinite(local_incoming[j])||local_incoming[j]<0)return -5;
    int column=entry_surface*nz+j;
    incoming_sum[column]+=angular_track_weight*local_incoming[j];
    for(int i=0;i<nz;++i)for(int c=0;c<k;++c) {
      const double value=local_transfer[(i*nz+j)*k+c];
      if(!std::isfinite(value)||value<0)return -5;
      int row=exit_surface*nz+i;
      transfer_sum[(row*nwhite+column)*k+c]+=angular_track_weight*value;
    }
    for(int side=0;side<2;++side)for(int r=0;r<8;++r)for(int c=0;c<k;++c) {
      const double value=local_leakage[((side*8+r)*nz+j)*k+c];
      if(!std::isfinite(value)||value<0)return -5;
      leakage_sum[((side*8+r)*nwhite+column)*k+c]+=angular_track_weight*value;
    }
  }
  // Output sums are allocated/zeroed once by the owning Python worker. It
  // checks every complete sum after ALL181824 real actions, without truncation.
  for(int i=0;i<6;++i)if(!std::isfinite(geometric[i]))return -6;
  return 0;
}
