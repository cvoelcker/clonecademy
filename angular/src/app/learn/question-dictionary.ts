import {AddMultiplyChoiceComponent} from './course-editor/add-multiply-choice/add-multiply-choice.component';
import {AddInformationTextComponent} from './course-editor/add-info-text/add-info-text.component';
import {AddInformationYoutubeComponent} from './course-editor/add-info-youtube/add-info-youtube.component';

import {MultipleChoiceQuestionComponent} from './multiple-choice-question/multiple-choice-question.component'
import {InformationTextComponent} from './info-text/info-text.component'
import {InformationYoutubeComponent} from './info-youtube/info-youtube.component'


export const QuestionDictionary = {
  detailComponents: [
    {
      name: 'Multiple Choice Question',
      key: 'multiple_choice',
      component: AddMultiplyChoiceComponent
    },
    {
      name: 'Information Text',
      key: 'info_text',
      component: AddInformationTextComponent
    },
    {
      name: 'Information Text (Youtube)',
      key: 'info_text_youtube',
      component: AddInformationYoutubeComponent
    }

  ],
  components: {
    'multiple_choice': MultipleChoiceQuestionComponent,
    'info_text': InformationTextComponent,
    'info_text_youtube': InformationYoutubeComponent,
  },
  questionComponents: [
    MultipleChoiceQuestionComponent,
    InformationTextComponent,
    InformationYoutubeComponent,
    AddMultiplyChoiceComponent,
    AddInformationTextComponent,
    AddInformationYoutubeComponent,
  ]
}
