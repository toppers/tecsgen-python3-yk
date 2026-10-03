#ifndef tAlarm_FACTORY_H
#define tAlarm_FACTORY_H
#include "kernel_id.h"
DeclareAlarm( AlarmCallbackButtonCheck );
DeclareAlarm( Bluetooth_AlarmTimeOut );
DeclareAlarm( DelayConnectBluetoothTask_Alarm );
DeclareAlarm( AVR_AlarmCallbackAVR );
DeclareAlarm( Button_AlarmCallbackButtonUpdate );
DeclareAlarm( RotaryEncoder_AlarmCallbackMotor );
DeclareAlarm( DelayStarterTask_Alarm );
DeclareAlarm( TailControllerTask_Alarm );
DeclareAlarm( BalancerTask_Alarm );
DeclareAlarm( LinetracerTask_Alarm );
#endif /* tAlarm_FACTORY_H */
