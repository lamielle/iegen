/*! \file
 
  ERG.h

  Prototypes for explicit relation generators.

*/

#include "util.h"
#include "ExplicitRelation.h"

void ERG_cpack(ExplicitRelation* relptr, ExplicitRelation* old2new);

void ERG_lexmin(ExplicitRelation* relptr, ExplicitRelation*  old2new);

void ERG_blockpart(int lb, int ub, int numpart, ExplicitRelation* part);

