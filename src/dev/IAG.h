/*! \file
 
  IAG.h

  Prototypes for index array generators.

*/

#include "util.h"
#include "ExplicitRelation.h"

void IAG_cpack(ExplicitRelation* relptr, ExplicitRelation* old2new);

void IAG_lexmin(ExplicitRelation* relptr, ExplicitRelation*  old2new);

