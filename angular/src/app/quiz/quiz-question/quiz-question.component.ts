import { Component, OnInit } from '@angular/core';
import { ServerService } from '../../service/server.service'
import { ActivatedRoute, Params, Router } from '@angular/router'

@Component({
  selector: 'app-quiz-question',
  templateUrl: './quiz-question.component.html',
  styleUrls: ['./quiz-question.component.scss']
})
/**
 * @author Leonhard Wiedmann
 *
 * A component that implements a quiz view
 */
export class QuizQuestionComponent implements OnInit {

  courseID: number = -1;
  quiz: number = -1;
  data = {}

  constructor(private router: Router, public server: ServerService, private route: ActivatedRoute) {

    this.load();
  }

  /**
  loads data from server for current quiz id (from url)
  @author Leonhard Wiedmann
  **/
  load(){
    this.route.params.subscribe((data: Params) => {
      this.courseID = Number(data.id)
      this.quiz = Number(data.quiz)
      this.server.get('courses/' + this.courseID + '/quiz/' + this.quiz + '/').then((data) => {
        this.data = data
      })
    })
  }

  ngOnInit() {
  }

  /**
  sends data to server for current this.data['answers'].chosen if it is true
  @author Leonhard Wiedmann
  **/
  submit(){
    let value = {}
    for(let i = 0; i < this.data['answers'].length; i++){
      if (this.data['answers'][i].chosen != undefined){
        value[this.data['answers'][i].id] = this.data['answers'][i].chosen
      }
      else {
        value[this.data['answers'][i].id] = false
      }
    }
    this.server.post('courses/' + this.courseID + '/quiz/' + this.quiz + '/', value).then((data) => {
      if(data['last']){
        this.router.navigateByUrl('/course')
        return;
      }
      else{
        this.quiz = Number(this.quiz) + 1
        this.router.navigateByUrl('course/quiz/'+this.courseID+'/' + this.quiz)
        this.load()
      }
    })
  }

}
