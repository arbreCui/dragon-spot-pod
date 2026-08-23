# Host tools for the SPOR64 iterative route.
#
# These host programs link the current Dragon/Ganlib libraries, so any
# change under ../../src leaves them stale.  A stale tool does not produce
# a wrong answer -- the lifecycle boundaries are fail-closed and it will
# hard-reject the archive instead -- but it costs a run to find out.
# Rebuild them with `make -C validation/iterative` after every src build.
#
# The flags are the protocol's canonical set.  -O2 introduces FMA
# contraction and has been observed to shift recomputed defects by 1 ULP,
# which breaks the bitwise receipts, so these tools are always -O0 with
# -ffp-contract=off.

ARCH    := $(shell uname -s)_$(shell uname -m)
ROOT    := ../..
DRAGON  := $(ROOT)/lib/$(ARCH)
GANLIB  := $(ROOT)/Ganlib/lib/$(ARCH)

FC      := gfortran
FFLAGS  := -std=f2008 -O0 -g -pedantic -Wall -Wextra -Werror \
           -Wno-compare-reals -fcheck=all -ffp-contract=off -fno-fast-math
INCLUDE := -I $(DRAGON)/modules -I $(GANLIB)/modules
LIBS    := $(DRAGON)/libDragon.a $(GANLIB)/libGanlib.a -lstdc++

TOOLS   := admit_candidate_radial close_r64_returned \
           check_convergence_gate check_one_map_xsm \
           prepare_r64_aa1_projected prepare_r64_next_projected

.PHONY: all tools b2c-runtime-dimensions clean
all: tools
tools: $(TOOLS)

b2c-runtime-dimensions:
	sh run_b2c_runtime_dimensions.sh

$(TOOLS): %: %.f90 $(DRAGON)/libDragon.a
	$(FC) $(FFLAGS) $(INCLUDE) $< $(LIBS) -o $@

clean:
	rm -f $(TOOLS)
