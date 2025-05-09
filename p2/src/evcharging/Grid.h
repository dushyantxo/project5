#ifndef GRID_H
#define GRID_H
#include <omnetpp.h>
class Grid : public omnetpp::cSimpleModule {
  protected:
    virtual void initialize() override;
    virtual void handleMessage(omnetpp::cMessage *msg) override;
};
#endif