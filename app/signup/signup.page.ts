import { Component, OnInit } from '@angular/core';
import { AngularFireAuth } from '@angular/fire/compat/auth';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.page.html',
  styleUrls: ['./signup.page.scss'],
})
export class SignupPage implements OnInit {

  email : string="";
  password: string="";
  confirmPassword: string="";

  constructor(private afAuth: AngularFireAuth, private router: Router) {}

  async signup() {
    if (this.password !== this.confirmPassword) {
      console.error('Passwords do not match!');
      // Display error message or show validation message to the user
      return;
    }

    try {
      const userCredential = await this.afAuth.createUserWithEmailAndPassword(this.email, this.password);
      console.log('User registered:', userCredential.user);
      this.router.navigate(['/login']);  // Navigate to login page after signup
    } catch (error) {
      console.error('Error during signup:', error);
      // Handle errors (e.g., show a message to the user)
    }
  }

  navigateTologin() {
    this.router.navigate(['/login']);
  }



  ngOnInit() {
  }

}
