#include "nemdef.h"

int foo(_secret int a, int b)
{
  int result = 3;

  if (a < b)
  {
    result = 7;
  }

  return result;
}
