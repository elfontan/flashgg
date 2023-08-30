#include "flashgg/DataFormats/interface/UntaggedTag.h"

using namespace flashgg;

UntaggedTag::UntaggedTag() : DiPhotonTagBase::DiPhotonTagBase() {}

UntaggedTag::~UntaggedTag() {}

UntaggedTag::UntaggedTag( edm::Ptr<flashgg::DiPhotonCandidate> diPho, edm::Ptr<DiPhotonMVAResult> mvaRes )
    : UntaggedTag::UntaggedTag( diPho, *mvaRes ) {}

UntaggedTag::UntaggedTag( edm::Ptr<flashgg::DiPhotonCandidate> diPho, edm::Ptr<DiPhotonMVAResult> mvaRes, edm::Ptr<DiPhotonMVAResult> mvaRes_DefLowMass, edm::Ptr<DiPhotonMVAResult> mvaRes_NewMcBdt, edm::Ptr<DiPhotonMVAResult> mvaRes_DataBdt )
    : UntaggedTag::UntaggedTag( diPho, *mvaRes, *mvaRes_DefLowMass, *mvaRes_NewMcBdt, *mvaRes_DataBdt ) {}

UntaggedTag::UntaggedTag( edm::Ptr<DiPhotonCandidate> dipho, DiPhotonMVAResult mvares ) 
    :  DiPhotonTagBase::DiPhotonTagBase( dipho, mvares ) {}

UntaggedTag::UntaggedTag( edm::Ptr<DiPhotonCandidate> dipho, DiPhotonMVAResult mvares, DiPhotonMVAResult mvares_DefLowMass, DiPhotonMVAResult mvares_NewMcBdt, DiPhotonMVAResult mvares_DataBdt ) 
    :  DiPhotonTagBase::DiPhotonTagBase( dipho, mvares, mvares_DefLowMass, mvares_NewMcBdt, mvares_DataBdt ) {}

UntaggedTag *UntaggedTag::clone() const
{
    std::cout << ">>> UntaggedTag.cc here" << endl;
    UntaggedTag *result = new UntaggedTag( *this );
    return result;
}
// Local Variables:
// mode:c++
// indent-tabs-mode:nil
// tab-width:4
// c-basic-offset:4
// End:
// vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

