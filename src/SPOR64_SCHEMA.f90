module SPOR64_SCHEMA
  ! The record inventories of every SPOR64 object, in one place.
  ! These name sets are the object model of the route: which records an
  ! object of each kind may carry, no more and no less.  They were
  ! previously hand-copied into the module that happened to check them,
  ! so adding one record meant editing several literal arrays and the
  ! edit could be forgotten in some of them.  EXACT_INVENTORY in
  ! SPOR64_VERIFY consumes these; each boundary still decides for itself
  ! which inventory applies to the object it is admitting.
  implicit none
  public

  character(len=12), parameter :: SCHEMA_PLANE_SEED_AUTHORITY(5) = &
        ['RHO         ','PLANE       ','FLUX        ','STATE       ', &
         'EPOCH       ']

  character(len=12), parameter :: SCHEMA_SOURCE_AUTHORITY(5) = &
        ['RHO         ','PLANE       ','STATE       ','QFISS       ', &
         'EPOCH       ']

  character(len=12), parameter :: SCHEMA_SYSTEM_AUTHORITY(3) = &
        ['RHO         ','STATE       ','EPOCH       ']

  character(len=12), parameter :: SCHEMA_ARCHIVE_ROOT_AUTHORITY(4) = &
        ['RHO         ','NPLANE      ','STATE       ','EPOCH       ']

  character(len=12), parameter :: SCHEMA_CLOSED_ARCHIVE_ROOT(8) = &
        ['SIGNATURE   ','LISTDIM     ','SPOT-ITER-K ','TRACK       ', &
         'MICROLIB2   ','SYSTEM      ','FLUX        ','SPOT-R64    ']

  character(len=12), parameter :: SCHEMA_SOLVED_AUTHORITY(5) = &
        ['FLUX        ','SOUR        ','RHO         ','STATE       ', &
         'EPOCH       ']

  character(len=12), parameter :: SCHEMA_PROJECTED_AUTHORITY(4) = &
        ['RHO         ','FLUX        ','STATE       ','EPOCH       ']

  character(len=12), parameter :: SCHEMA_PROJECTED_PLANE_ROOT(12) = &
        ['SPOT-R64    ','FLUX        ','SIGNATURE   ','STATE-VECTOR', &
         'EPS-CONVERGE','IMERGE-LEAK ','KEYFLX      ','OPTION      ', &
         'LINK.MACRO  ','LINK.TRACK  ','LINK.SYSTEM ','SPOT-LEAK1D ']

  character(len=12), parameter :: SCHEMA_PROJECTED_PLANE_ROOT_L64(13) = &
        ['SPOT-R64    ','FLUX        ','SIGNATURE   ','STATE-VECTOR', &
         'EPS-CONVERGE','IMERGE-LEAK ','KEYFLX      ','OPTION      ', &
         'LINK.MACRO  ','LINK.TRACK  ','LINK.SYSTEM ','SPOT-LEAK1D ', &
         'LEAK1D64    ']

  character(len=12), parameter :: SCHEMA_RESPONSE_GROUP_PHYS(15) = &
        ['CF$MCCG     ','ILUDF$MCCG  ','CQ$MCCG     ','DIAGQ$MCCG  ', &
         'PJJ$MCCG    ','PJJX$MCCG   ','PJJY$MCCG   ','PJJZ$MCCG   ', &
         'PJJXI$MCCG  ','PJJYI$MCCG  ','PJJZI$MCCG  ','DRAGON-TXSC ', &
         'SPOT-S0-PHYS','DRAGON-S0XSC','DIAGF$MCCG  ']

  character(len=12), parameter :: SCHEMA_RESPONSE_GROUP(12) = &
        ['CF$MCCG     ','ILUDF$MCCG  ','CQ$MCCG     ','DIAGQ$MCCG  ', &
         'PJJ$MCCG    ','PJJX$MCCG   ','PJJY$MCCG   ','PJJZ$MCCG   ', &
         'PJJXI$MCCG  ','PJJYI$MCCG  ','PJJZI$MCCG  ','DIAGF$MCCG  ']

  character(len=12), parameter :: SCHEMA_PROJECTED_ARCHIVE_ROOT(7) = &
        ['SIGNATURE   ','LISTDIM     ','SPOT-ITER-K ','TRACK       ', &
         'MICROLIB2   ','FLUX        ','SPOT-R64    ']

  character(len=12), parameter :: SCHEMA_CANDIDATE_SYSTEM_ROOT(7) = &
        ['SIGNATURE   ','LINK.MACRO  ','LINK.TRACK  ','STATE-VECTOR', &
         'SPOT-LEAK1D ','SPOT-L1-SNAP','GROUP       ']

  character(len=12), parameter :: SCHEMA_CANDIDATE_SYSTEM_ROOT_L1RAW(8) = &
        ['SIGNATURE   ','LINK.MACRO  ','LINK.TRACK  ','STATE-VECTOR', &
         'SPOT-LEAK1D ','SPOT-L1-SNAP','GROUP       ','SPOT-L1-RAW ']

  character(len=12), parameter :: SCHEMA_SYSTEM_ROOT(8) = &
        ['SIGNATURE   ','LINK.MACRO  ','LINK.TRACK  ','STATE-VECTOR', &
         'SPOT-LEAK1D ','SPOT-L1-SNAP','GROUP       ','SPOT-R64    ']

  character(len=12), parameter :: SCHEMA_SYSTEM_ROOT_L1RAW(9) = &
        ['SIGNATURE   ','LINK.MACRO  ','LINK.TRACK  ','STATE-VECTOR', &
         'SPOT-LEAK1D ','SPOT-L1-SNAP','GROUP       ','SPOT-R64    ', &
         'SPOT-L1-RAW ']

  character(len=12), parameter :: SCHEMA_SOLVED_ROOT(14) = &
        ['SPOT-R64    ','FLUX        ','SOUR        ','SIGNATURE   ', &
         'STATE-VECTOR','EPS-CONVERGE','IMERGE-LEAK ','KEYFLX      ', &
         'OPTION      ','LINK.MACRO  ','LINK.TRACK  ','LINK.SYSTEM ', &
         'SPOT-LEAK1D ','LEAK1D64    ']

  character(len=12), parameter :: SCHEMA_SOLVED_PLANE_AUTHORITY(6) = &
        ['RHO         ','PLANE       ','FLUX        ','SOUR        ', &
         'STATE       ','EPOCH       ']

  character(len=12), parameter :: SCHEMA_SOURCE_ROOT(7) = &
        ['SIGNATURE   ','STATE-VECTOR','SPOT-FROZEN ','SPOT-KEFF   ', &
         'SPOT-QINT   ','DSOUR       ','SPOT-R64    ']

  character(len=12), parameter :: SCHEMA_FEEDBACK_ROOT(9) = &
        ['SIGNATURE   ','LISTDIM     ','SPOT-ITER-K ','SPOT-L1-ERR ', &
         'TRACK       ','MICROLIB2   ','SYSTEM      ','FLUX        ', &
         'SPOT-R64    ']

  character(len=12), parameter :: SCHEMA_RETURNED_FEEDBACK_ROOT(7) = &
        ['SIGNATURE   ','LISTDIM     ','TRACK       ','MICROLIB2   ', &
         'SYSTEM      ','FLUX        ','SPOT-R64    ']

  character(len=12), parameter :: SCHEMA_RETURNED_ROOT_AUTHORITY(3) = &
        ['NPLANE      ','STATE       ','EPOCH       ']

  character(len=12), parameter :: SCHEMA_RETURNED_CHILD_ROOT(17) = &
        ['SPOT-R64    ','FLUX        ','SOUR        ','SIGNATURE   ', &
         'STATE-VECTOR','EPS-CONVERGE','IMERGE-LEAK ','KEYFLX      ', &
         'OPTION      ','LINK.MACRO  ','LINK.TRACK  ','LINK.SYSTEM ', &
         'SPOT-LEAK1D ','LEAK1D64    ','SPOT-FS-EQN ','SPOT-FS-K   ', &
         'SPOT-QFISS  ']

  character(len=12), parameter :: SCHEMA_RETURNED_CHILD_AUTHORITY(6) = &
        ['RHO         ','FLUX        ','SOUR        ','QFISS       ', &
         'STATE       ','EPOCH       ']

end module SPOR64_SCHEMA
