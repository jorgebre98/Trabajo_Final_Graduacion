/* ========================================
 *
 * Copyright Jorge Brenes Alfaro, 2022
 * All Rights Reserved
 * UNPUBLISHED, LICENSED SOFTWARE.
 *
 * UART COMUNICATION
 *
 * ========================================
*/
#include <project.h>
#include "stdio.h"
#include <stdbool.h>

int pwm_value; // Valor recibido para escribir en el PWM.
int angle_Quad; // Lectura del decodificador de cuadratura.
bool runcode = false; // Para iniciar/detener el proceso dentro de la interrupción se puede activar/apagar desde el switch principal (case)

CY_ISR_PROTO(isr_Control_Handler);
CY_ISR(isr_Control_Handler){
    if (runcode == true){
        CyPins_SetPin(LED_EJECUCION_0); // Enciende al iniciar la interrupción (Activo en bajo)
        PWM_1_WriteCompare(pwm_value); // Escribe el valor de pwm.
        angle_Quad = QuadDec_1_GetCounter(); // Obtiene valor del decodificador.
        CyPins_ClearPin(LED_EJECUCION_0);
    }
}
                    
int main(void)
{
    CyGlobalIntEnable; // Enable global interrupts.
    
    /*START COMPONENTS*/
    UART_1_Start();
    PWM_1_Start();
    QuadDec_1_Start();
    Timer_1_Start();
    isr_control_StartEx(isr_Control_Handler);
    
    UART_1_ClearRxBuffer(); 
    UART_1_ClearTxBuffer();
    
    int32 entero;
    uint8* arr = &entero;
    
    for (;;){
        runcode = true;
        pwm_value = UART_1_ReadRxData();
        for (int cont=0;cont<4;cont++){
            arr[cont] = angle_Quad;
        }
        UART_1_PutArray((uint8*)arr,4);
        //UART_1_PutArray((uint8*)angle_Quad,4);
        CyDelay(20);
    }
}