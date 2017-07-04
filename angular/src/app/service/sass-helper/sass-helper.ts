import { Component, ViewChild, ElementRef } from '@angular/core';

export const PREFIX = '--';

@Component({
    selector: 'sass-helper',
    template: '<div #component></div>',
    styleUrls: ['./sass-helper.scss']
})
export class SassHelperComponent {

    @ViewChild('component') element:ElementRef;

    constructor() {

    }

    // Read the custom property of body section with given name:
    readProperty(name: string): string {
        let bodyStyles = window.getComputedStyle(this.element.nativeElement)
        return bodyStyles.getPropertyValue(PREFIX + name);
    }
}
