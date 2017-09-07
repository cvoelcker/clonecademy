import { trigger, state, style, animate, transition } from '@angular/animations';

export const slideIn = trigger('slideIn', [
      state('1', style({
        'display': 'block',
        'overflow': 'hidden',
      })),
      state('0', style({
        'display': 'none',
        'overflow': 'hidden',
      })),
      transition('1 => 0', [
          style({ height: '*' }),
          animate(250, style({ height: 0 }))
      ]),
      transition('* => 1', [
          style({ height: '0' }),
          animate(250, style({ height: '*' })),
  ]),
])

export const menuSlideIn = trigger('slideIn', [
    state('1', style({ 'height': '*', 'overflow-y': 'hidden' })),
    state('0', style({ 'height': '0',  'overflow-y': 'hidden' })),
    transition('1 => 0', [
        style({ height: '*' }),
        animate(250, style({ height: 0 }))
    ]),
    transition('0 => 1', [
        style({ height: '0' }),
        animate(250, style({ height: '*' })),
]),
])
