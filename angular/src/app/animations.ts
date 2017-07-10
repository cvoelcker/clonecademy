import { trigger, state, style, animate, transition } from '@angular/animations';

export const slideIn = trigger('slideIn', [
      state('1', style({
        'overflow': 'hidden',
      })),
      state('0', style({
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
