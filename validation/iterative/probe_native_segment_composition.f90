program probe_native_segment_composition
  ! Private probe linked to the sealed native libraries; no replacement kernels.
  use, intrinsic :: iso_fortran_env, only: int32,real32,real64
  implicit none
  integer :: input,output,i,j,count,magic
  integer :: nom_sc(3),nom_ds(3),zone(3),is(3),js(1),ka(1),pjjind(1,2)
  real(real32) :: total(0:1),psj(1),trhar(1,1,1)
  real(real64) :: record(2),h(3),b(3),pjj(1,1),values(3,6),fractions(6)
  character(len=1024) :: input_path,output_path
  if(command_argument_count()/=2) error stop 'usage: probe INPUT OUTPUT'
  call get_command_argument(1,input_path);call get_command_argument(2,output_path)
  open(newunit=input,file=trim(input_path),status='old',action='read',access='stream',form='unformatted')
  read(input) magic,count
  if(magic/=290929.or.count<1) error stop 'invalid request'
  open(newunit=output,file=trim(output_path),status='new',access='stream',form='unformatted')
  write(output) 290930,count,6
  fractions=[1.0_real64,.5_real64,.25_real64,.125_real64,1.0_real64/3,2.0_real64/3]
  nom_sc=[-1,1,-2];nom_ds=[2,1,3];zone=[1,-1,-1]
  is=0;js=0;ka=1;pjjind=1;trhar=1;total=0
  call XDRTA2
  do i=1,count
    read(input) record
    if(record(1)<0.or.record(2)<=0) error stop 'invalid coefficients'
    total(1)=real(record(1),real32)
    if(real(total(1),real64)/=record(1)) error stop 'total precision changed'
    do j=1,6
      h=0;h(2)=record(2)*fractions(j);b=0;pjj=0;psj=0
      call MCGSCA(3,3,1,nom_sc,zone,h,total,b)
      call MCGDSCA(1,3,1,0,is,js,h,ka,nom_ds,zone,total,1.0_real64, &
        3,1,pjj,psj,1,1,1,1,1,trhar,.false.,pjjind)
      values(:,j)=[1.0_real64-real(total(1),real64)*b(2),b(2),pjj(1,1)]
    enddo
    write(output) values
  enddo
  close(input);close(output)
end program
