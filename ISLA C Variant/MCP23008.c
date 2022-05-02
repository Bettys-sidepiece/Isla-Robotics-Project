#include "MCP23008.h"
#include "hardware/gpio.h"
#include "pico/stdlib.h"

MCP23008::mcp23008_init(i2c_inst_t *_i2c, uint8_t _address) : i2c(_i2c), address(_address){

}

int MCP23008::write_to_register(uint8_t reg, uint8_t value){
    uint8_t command[] = {reg, value};
    int result = i2c_write_blocking(i2c, address, command, 2, false);
    if(result == PICO_ERROR_GENERIC){
        return result;
    }
    return PICO_ERROR_NONE;
}

int MCP23008::read_from_register(uint8_t reg) {
	uint8_t buffer = 0;
	int result;
	result = i2c_write_blocking(i2c, address,  &reg, 1, true);
	if (result == PICO_ERROR_GENERIC) {
		return result;
	}

	result = i2c_read_blocking(i2c, address, &buffer, 1, false);
	if (result == PICO_ERROR_GENERIC)
		return result;

	return buffer;
}

int MCP23008::setup(bool mirroring, bool polarity) {
	int result;
	result = setup_bank_configuration(REG_IOCON, mirroring, polarity);
	if (result != 0)
		return PICO_ERROR_GENERIC;
	return result;
}

int MCP23008::setup_bank_configuration(int reg, bool mirroring, bool polarity) {
	int ioConValue = 0;
    set_bit(ioConValue, 7, false);
    set_bit(ioConValue, 6, false);
	set_bit(ioConValue, 5,false); //MCP23008_IOCON_SEQOP_BIT,
	set_bit(ioConValue, 4, false); //MCP23008_IOCON_DISSLW_BIT
	set_bit(ioConValue, 3, false); //MCP23008_IOCON_HAEN_BIT
	set_bit(ioConValue, 2, false); //MCP23008_IOCON_ODR_BIT
	set_bit(ioConValue, 1, polarity); //MCP23008_IOCON_INTPOL_BIT
    set_bit(ioConValue, 0, false);
	return write_register(reg, ioConValue);
}
int MCP23008::get_last_interrupt_pin() {
	int intFlag;

	intFlag = read_dual_registers(REG_INTF);
	if (intFlag != PICO_ERROR_GENERIC) {
		for (int i = 0; i < 16; i++) {
			if (is_bit_set(intFlag, i)) {
				return i;
			}
		}
	} 

	return PICO_ERROR_GENERIC;
}

int MCP23008::get_interrupt_values() {
	return read_dual_registers(REG_INTCAP);
}

int MCP23008::update_input_values() {
	int result = read_dual_registers(REG_GPIO);
	if (result != PICO_ERROR_GENERIC) {
		last_input = result;
		result = PICO_ERROR_NONE;
	}
	return result;
}

bool MCP23008::get_input_pin_value(int pin) const {
	return is_bit_set(last_input, pin);
}

int MCP23008::get_address() const {
	return address;
}

int MCP23008::set_io_direction(int direction) {
	return write_dual_registers(REG_IODIR, direction);
}

int MCP23008::set_pullup(int direction) {
	return write_dual_registers(REG_GPPU, direction);
}

int MCP23008::set_interrupt_type(int compare_to_reg) {
	return write_dual_registers(REG_INTCON, compare_to_reg);
}

int MCP23008::enable_interrupt(int enabled) {
	return write_dual_registers(REG_GPINTEN, enabled);
}

int MCP23008::set_all_output_bits(int all_bits) {
	output = all_bits;
	return write_dual_registers(REG_GPIO, all_bits); 
}

void MCP23008::set_output_bit_for_pin(int pin, bool set) {
	set_bit(output, pin, set);
}

bool MCP23008::get_output_bit_for_pin(int pin) const {
	return is_bit_set(output, pin);
}

int MCP23008::flush_output() {
	return write_dual_registers(REG_GPIO, output);
}