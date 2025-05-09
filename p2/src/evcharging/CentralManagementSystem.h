#ifndef CENTRALMANAGEMENTSYSTEM_H
#define CENTRALMANAGEMENTSYSTEM_H
#include <omnetpp.h>
class CentralManagementSystem : public omnetpp::cSimpleModule {
  protected:
    virtual void initialize() override;
    virtual void handleMessage(omnetpp::cMessage *msg) override;
};
#endif