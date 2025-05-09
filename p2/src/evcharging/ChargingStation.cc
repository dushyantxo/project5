#include <omnetpp.h>
using namespace omnetpp;

class ChargingStation : public cSimpleModule {
    cMessage *pendingPowerRequest = nullptr;

protected:
    virtual void handleMessage(cMessage *msg) override {
        if (strcmp(msg->getName(), "AuthenticationResponse") == 0) {
            EV << "Authentication successful, requesting power delivery.\n";
            cMessage *powerMsg = new cMessage("PowerDeliveryRequest");
            send(powerMsg, "out");
            delete msg;
        } else {
            EV << "Received from EV: " << msg->getName() << "\n";
            // Simulate extracting SOC (not parsed, just for show)
            EV << "Forwarding AuthenticationRequest to CMS\n";
            cMessage *auth = new cMessage("AuthenticationRequest");
            send(auth, "cmpOut");
            delete msg;
        }
    }
};

Define_Module(ChargingStation);
