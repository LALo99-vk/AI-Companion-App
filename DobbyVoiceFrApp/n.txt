import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AlertController } from '@ionic/angular';


@Component({
  selector: 'app-tab2',
  templateUrl: 'tab2.page.html',
  styleUrls: ['tab2.page.scss']
})
export class Tab2Page {

  symptoms: string = ''; // String to store the user's input symptoms

  constructor(private http: HttpClient, private alertController: AlertController) {}

  async submitSymptoms() {
    if (this.symptoms.trim() === '') {
      const alert = await this.alertController.create({
        header: 'Error',
        message: 'Please enter your symptoms.',
        buttons: ['OK'],
      });
      await alert.present();
      return;
    }

    const payload = {
      symptoms: this.symptoms,
    };

    // Send POST request to Flask backend
    this.http.post('http://127.0.0.1:5000/predict', payload).subscribe(
      async (response: any) => {
        // Handle the successful response
        console.log('Response from server:', response);
        const alert = await this.alertController.create({
          header: 'Prediction',
          message: `Disease: ${response.disease}\nDiet: ${response.diet.join(', ')}\nMedications: ${response.medications.join(', ')}\nPrecautions: ${response.precautions.join(', ')}\nWorkout: ${response.workout.join(', ')}`,
          buttons: ['OK'],
        });
        await alert.present();
      },
      async (error) => {
        // Handle the error
        console.error('Error from server:', error);
        const alert = await this.alertController.create({
          header: 'Error',
          message: 'Failed to get prediction. Please try again later.',
          buttons: ['OK'],
        });
        await alert.present();
      }
    );
  }
}


  


