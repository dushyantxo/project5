#ifndef CHARGINGSTATION_H
#define CHARGINGSTATION_H
#include <omnetpp.h>
class ChargingStation : public omnetpp::cSimpleModule {
  protected:
    virtual void initialize() override;
    virtual void handleMessage(omnetpp::cMessage *msg) override;
};
#endif