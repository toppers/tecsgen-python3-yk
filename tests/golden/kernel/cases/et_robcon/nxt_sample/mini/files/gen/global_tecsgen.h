/*
 * このファイルは tecsgen により自動生成されました
 * このファイルを編集して使用することは、意図されていません
 */
#ifndef GLOBAL_TECSGEN_H
#define GLOBAL_TECSGEN_H


/* import_C により import されるヘッダ #_IMP_# */
#include "tecs_kernel.h"
/**/

#ifndef TOPPERS_MACRO_ONLY

struct TAG__0__ {
                uint8_t        power;
                uint8_t        pwm_frequency;
                int8_t         output_percent[4];
                uint8_t        output_mode;
                uint8_t        input_power;
};
typedef struct TAG__0__ TOAVR;
struct TAG__1__ {
                uint16_t       adc_value[4];
                uint16_t       buttons;
                uint16_t       battery_is_AA;
                uint16_t       battery_mV;
                uint8_t        avr_fw_version_major;
                uint8_t        avr_fw_version_minor;
};
typedef struct TAG__1__ FROMAVR;
struct i2cPartialTransaction {
                uint8_t        start;
                uint8_t        restart;
                uint8_t        stop;
                uint8_t        tx;
                uint8_t        lastPT;
                uint16_t       size;
                uint8_t*       data;
};
typedef struct i2cPartialTransaction I2CPT;
 extern void tCPU_CB_initialize();
 extern void tKernel_CB_initialize();
 extern void tApplicationMode_CB_initialize();
 extern void tTask_CB_initialize();
 extern void tISR_CB_initialize();
 extern void tCounter_CB_initialize();
 extern void tAlarm_CB_initialize();
 extern void tResource_CB_initialize();
 extern void tConfigInterrupt_CB_initialize();
 extern void tTWIBody_CB_initialize();
 extern void tAVRBody_CB_initialize();
 extern void tSPIBody_CB_initialize();
 extern void tLCD_CB_initialize();
 extern void tDisplayBody_CB_initialize();
 extern void tButtonBody_CB_initialize();
 extern void tBattery_CB_initialize();
 extern void tCheckNXTButtonBody_CB_initialize();
 extern void tSystemTimer_CB_initialize();
 extern void tSampleTaskBody_CB_initialize();
 extern void tSampleAlarmBody_CB_initialize();

#define INITIALIZE_TECS() \
 	tCPU_CB_initialize();\
 	tKernel_CB_initialize();\
 	tApplicationMode_CB_initialize();\
 	tTask_CB_initialize();\
 	tISR_CB_initialize();\
 	tCounter_CB_initialize();\
 	tAlarm_CB_initialize();\
 	tResource_CB_initialize();\
 	tConfigInterrupt_CB_initialize();\
 	tTWIBody_CB_initialize();\
 	tAVRBody_CB_initialize();\
 	tSPIBody_CB_initialize();\
 	tLCD_CB_initialize();\
 	tDisplayBody_CB_initialize();\
 	tButtonBody_CB_initialize();\
 	tBattery_CB_initialize();\
 	tCheckNXTButtonBody_CB_initialize();\
 	tSystemTimer_CB_initialize();\
 	tSampleTaskBody_CB_initialize();\
 	tSampleAlarmBody_CB_initialize();\
/* INITIALIZE_TECS terminator */

#define INITIALZE_TECSGEN() INITIALIZE_TECS()  /* for backward compatibility */

/* Descriptor for dynamic join */
#define Descriptor( signature_global_name )  DynDesc__ ## signature_global_name
#define is_descriptor_unjoined( desc )  ((desc).vdes==NULL)

#endif /* TOPPERS_MACRO_ONLY */

#define NXT_PORT_A     ((const uint8_t)0)
#define NXT_PORT_B     ((const uint8_t)1)
#define NXT_PORT_C     ((const uint8_t)2)
#define NXT_PORT_S1    ((const uint8_t)0)
#define NXT_PORT_S2    ((const uint8_t)1)
#define NXT_PORT_S3    ((const uint8_t)2)
#define NXT_PORT_S4    ((const uint8_t)3)
#define NXT_AVR_ADDRESS ((const uint8_t)1)
#define NXT_AVR_N_INPUTS ((const uint8_t)4)
#define NXT_AVR_N_OUTPUTS ((const uint8_t)4)
#define MOTOR_A0       ((const uint32_t)15)
#define MOTOR_B0       ((const uint32_t)26)
#define MOTOR_C0       ((const uint32_t)0)
#define MOTOR_A1       ((const uint32_t)1)
#define MOTOR_B1       ((const uint32_t)9)
#define MOTOR_C1       ((const uint32_t)8)
#define MOTOR_PIN_MASK ((const uint32_t)67142403)
#define MOTOR_INTERRUPT_PINS ((const uint32_t)67141633)

#endif /* GLOBAL_TECSGEN_H */
