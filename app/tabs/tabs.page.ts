import { Component } from '@angular/core';
import {SpeechRecognition} from '@capacitor-community/speech-recognition'
import { Router } from '@angular/router';


@Component({
  selector: 'app-tabs',
  templateUrl: 'tabs.page.html',
  styleUrls: ['tabs.page.scss']
})
export class TabsPage {

  constructor(private router:Router) {}
   
}