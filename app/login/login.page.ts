import { Component, OnInit } from '@angular/core';

import { AngularFireAuth, AngularFireAuthModule } from '@angular/fire/compat/auth';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage {

  email: string="";
  password: string="";

  constructor(private afAuth: AngularFireAuth, private router: Router) {}


  async login() {

    try {
      const userCredential = await this.afAuth.signInWithEmailAndPassword(this.email, this.password);
      console.log('User logged in:', userCredential.user);
      this.router.navigate(['/tabs']); // Navigate to the tabs page after login
    } catch (error: unknown) {
      // Handle different errors
      if (error instanceof Error) {
        console.error('Error logging in:', error.message);
        let errorMessage = 'An error occurred. Please try again.';
        if ((error as any).code === 'auth/wrong-password') {
          errorMessage = 'Invalid password. Please try again.';
        } else if ((error as any).code === 'auth/user-not-found') {
          errorMessage = 'No user found with this email.';
        }
        alert(errorMessage);
      } else {
        console.error('Unexpected error:', error);
        alert('An unexpected error occurred. Please try again later.');
      }
    }
  }

  navigateTosignup() {
    this.router.navigate(['/signup']);
  }
  

}
