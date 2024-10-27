/** @odoo-module **/

import { registry } from "@web/core/registry";
import { usePopover } from "@web/core/popover/popover_hook";
import { Component } from "@odoo/owl";

export class AgePopover extends Component {
    setup() {
    }
}

AgePopover.template = "your_module.AgePopover"; // Define the template for the popover

export class AgeWidget extends Component {
    setup() {
        this.popover = usePopover(AgePopover, { position: "top" });
        this.dob = ""; // Initialize date of birth
        this.age = { years: 0, months: 0, days: 0 }; // Initialize age
        this.is_month = false; // Toggle for months
        this.is_day = false; // Toggle for days
    }

    // Show the popover with calculated age data
    showPopup(ev) {
        this.popover.open(ev.currentTarget, {
            dob: this.dob,
            age: this.age,
            is_month: this.is_month,
            is_day: this.is_day,
        });
    }

    // Calculate age from the date of birth
    calculateAge(dob) {
        if (!dob) return { years: 0, months: 0, days: 0 }; // If no DOB is provided, return zeroes

        const dobDate = new Date(dob);
        const today = new Date();

        let years = today.getFullYear() - dobDate.getFullYear();
        let months = today.getMonth() - dobDate.getMonth();
        let days = today.getDate() - dobDate.getDate();

        if (days < 0) {
            months--;
            days += new Date(today.getFullYear(), today.getMonth(), 0).getDate(); // Get days in previous month
        }

        if (months < 0) {
            years--;
            months += 12; // Adjust months to be within 0-11
        }

        return { years, months, days }; // Return the calculated age object
    }

    // Handle date of birth change event
    onDobChange(ev) {
        this.dob = ev.target.value; // Update the DOB
        this.age = this.calculateAge(this.dob); // Recalculate the age
    }

    // Toggle visibility of months in age
    toggleMonths() {
        this.is_month = !this.is_month; // Toggle the month display
    }

    // Toggle visibility of days in age
    toggleDays() {
        this.is_day = !this.is_day; // Toggle the day display
    }
}

AgeWidget.template = "your_module.AgeWidget"; // Define the template for the widget
AgeWidget.components = { Popover: AgePopover }; // Set the popover as a component

export const AgeCountWidget = {
    component: AgeWidget,
};

// Register the widget to the Odoo view
registry.category("fields").add("age_count_widget", AgeCountWidget);
