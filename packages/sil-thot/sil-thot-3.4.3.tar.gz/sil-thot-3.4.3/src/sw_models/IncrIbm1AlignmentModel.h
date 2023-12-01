#pragma once

#include "sw_models/Ibm1AlignmentModel.h"
#include "sw_models/IncrAlignmentModel.h"
#include "sw_models/IncrIbm1AlignmentTrainer.h"
#include "sw_models/anjiMatrix.h"

class IncrIbm1AlignmentModel : public Ibm1AlignmentModel, public virtual IncrAlignmentModel
{
public:
  IncrIbm1AlignmentModel();

  AlignmentModelType getModelType() const override
  {
    return IncrIbm1;
  }

  // Function to set a maximum size for the vector of expected
  // values anji (by default the size is not restricted)
  void set_expval_maxnsize(unsigned int _anji_maxnsize) override;

  void startIncrTraining(std::pair<unsigned int, unsigned int> sentPairRange, int verbosity = 0) override;
  void incrTrain(std::pair<unsigned int, unsigned int> sentPairRange, int verbosity = 0) override;
  void endIncrTraining() override;

  bool load(const char* prefFileName, int verbose = 0) override;
  bool print(const char* prefFileName, int verbose = 0) override;

  void clear() override;
  void clearTempVars() override;

  virtual ~IncrIbm1AlignmentModel()
  {
  }

protected:
  anjiMatrix anji;
  IncrIbm1AlignmentTrainer trainer;
};
