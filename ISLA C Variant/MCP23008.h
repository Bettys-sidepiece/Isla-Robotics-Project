#ifndef MCP23008_H
#define MCP23008_H

#include "hardware/i2c.h"
#include "hardware/gpio.h"
#include "pico/time.h"

#define REG_ADDRESS 0x20
#define REG_IPOL 0x01
#define REG_GPINTEN 0x02
#define REG_DEFVAL 0x03
#define REG_INTCON 0x04
#define REG_IOCON 0x05
#define REG_GPPU 0x06
#define REG_INTF 0x07
#define REG_INTCAP 0x08 //Read Only
#define REG_GPIO 0x09
#define REG_OLAT 0x0A 

inline void set_bit(int &value, int bit, bool set) {
	if (bit >= 0 && bit <= 7 {
		if (set) {
			value |= (1 << bit);
		} else {
			value &= ~(1 << bit);
		}
	}
}

inline bool is_bit_set(int value, int bit) {
	if (bit >= 0 && bit <= 7) {
		return (bool) (0x1 & (value >> bit));
	}
	return false;

static bool mcp23008_init(uint8_t address, i2c_inst_t *i2c);

static int mcp_setup(bool mirroring, bool polarity);

int get_last_interrupt pin();

int set_io_direction(int direction);

int set_pullup(int direction);

int set_interrupt_type(int compare_to_reg);

int enable_interrupt(int enabled);

int set_all_outputs_bits(int all_bits);

void set_output_bit_for_pin(int pin, bool set);

bool get_output_bit_for_pin(int pin) const;

	/**
	 * Flushes the internal output state to the device
	 * @return PICO_ERROR_NONE or PICO_ERROR_GENERIC
	 */

int flush_output();

int setup_bank_configuration(int reg, bool mirroring, bool polarity);

int write_to_reg(uint8_t reg, uint8_t value);

int read_from_register(uint8_t reg);

int read_dual_registers(uint8_t reg);

int write_dual_registers(uint8_t reg, int value);

#endif //MCP23008