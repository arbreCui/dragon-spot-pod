#include <stdio.h>

#include "cle2000.h"

int main(int argc, char **argv)
{
  FILE *input;
  kdi_file *object;
  int_32 rc;
  int_32 close_rc;

  if (argc != 3) return 64;
  input = fopen(argv[1], "r");
  if (input == NULL) return 65;
  object = kdiop_c(argv[2], 0);
  if (object == NULL) {
    fclose(input);
    return 66;
  }
  rc = clepil(input, stdout, object, clecst);
  fclose(input);
  if (rc == 0) rc = objpil(object, stdout, 0);
  close_rc = kdicl_c(object, rc == 0 ? 1 : 2);
  return rc != 0 ? (int)rc : (int)close_rc;
}
