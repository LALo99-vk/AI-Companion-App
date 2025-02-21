import { Component, OnInit, OnDestroy } from '@angular/core';
import { SpeechRecognition } from '@capacitor-community/speech-recognition';
import { CallNumber } from '@ionic-native/call-number/ngx';
import { Geolocation } from '@capacitor/geolocation';
import { Platform } from '@ionic/angular';
import { Toast } from '@capacitor/toast';

@Component({
  selector: 'app-emergency',
  templateUrl: './emergency.page.html',
  styleUrls: ['./emergency.page.scss'],
})
export class EmergencyPage implements OnInit, OnDestroy {
  isListening = false;
  private emergencyContact = '+91 9110282364';
  private speechListener: any;
  private retryAttempts = 0;
  private maxRetries = 3;
  private recognitionTimeout: any;

  constructor(
    private callNumber: CallNumber,
    private platform: Platform
  ) {}

  ngOnInit() {
    this.setupPermissions();
  }

  ngOnDestroy() {
    this.cleanup();
  }

  private cleanup(): void {
    this.cleanupListeners();
    if (this.recognitionTimeout) {
      clearTimeout(this.recognitionTimeout);
    }
    this.isListening = false;
  }

  async startSpeechRecognition(): Promise<void> {
    if (this.isListening) {
      return;
    }

    try {
      const setupSuccess = await this.setupPermissions();
      if (!setupSuccess) {
        return;
      }

      this.isListening = true;
      this.retryAttempts = 0;
      await this.initiateSpeechRecognition();
      
    } catch (error) {
      console.error('Start recognition error:', error);
      this.cleanup();
      await this.showToast('Failed to start listening');
    }
  }

  async stopSpeechRecognition(): Promise<void> {
    try {
      this.cleanup();
      await SpeechRecognition.stop();
      await this.showToast('Emergency detection stopped');
    } catch (error) {
      console.error('Stop recognition error:', error);
    }
  }

  private async setupPermissions(): Promise<boolean> {
    try {
      // Request location permission
      const locationStatus = await Geolocation.checkPermissions();
      if (locationStatus.location === 'denied') {
        await Geolocation.requestPermissions();
      }
      
      const { available } = await SpeechRecognition.available();
      if (!available) {
        await this.showToast('Speech recognition not available');
        return false;
      }

      await SpeechRecognition.requestPermissions();
      return true;
    } catch (error) {
      console.error('Permission setup error:', error);
      await this.showToast('Permission setup failed');
      return false;
    }
  }

  private cleanupListeners(): void {
    if (this.speechListener) {
      this.speechListener.remove();
      this.speechListener = null;
    }
  }

  private async initiateSpeechRecognition(): Promise<void> {
    try {
      this.cleanupListeners();
      await this.showToast('Listening for emergency commands...');

      await SpeechRecognition.start({
        language: 'en-US',
        partialResults: true,
        popup: false,
      });

      this.speechListener = SpeechRecognition.addListener('partialResults', async (data: any) => {
        if (!data.value || !Array.isArray(data.value)) return;

        const helpDetected = data.value.some((phrase: string) => 
          phrase.toLowerCase().includes('help me')
        );

        if (helpDetected) {
          await this.triggerEmergency();
        }
      });

      // Set timeout to restart recognition periodically
      this.recognitionTimeout = setTimeout(() => {
        if (this.isListening) {
          this.restartRecognition();
        }
      }, 10000);

    } catch (error) {
      console.error('Speech recognition setup error:', error);
      if (this.retryAttempts < this.maxRetries) {
        this.retryAttempts++;
        setTimeout(() => {
          this.initiateSpeechRecognition();
        }, 1000);
      } else {
        this.cleanup();
        await this.showToast('Failed to initialize speech recognition');
      }
    }
  }

  private async restartRecognition(): Promise<void> {
    try {
      await SpeechRecognition.stop();
      await this.initiateSpeechRecognition();
    } catch (error) {
      console.error('Restart error:', error);
    }
  }

  async triggerEmergency(): Promise<void> {
    try {
      // If speech recognition is running, stop it
      if (this.isListening) {
        await this.stopSpeechRecognition();
      }
      
      await this.showToast('Initiating emergency response...');
      
      // Get location first
      let locationUrl = '';
      try {
        const position = await Geolocation.getCurrentPosition({
          enableHighAccuracy: true,
          timeout: 10000
        });
        locationUrl = `https://maps.google.com/?q=${position.coords.latitude},${position.coords.longitude}`;
        console.log('Location:', locationUrl);
        await this.showToast(`Location captured: ${locationUrl}`);
      } catch (error) {
        console.error('Location error:', error);
        await this.showToast('Could not get location, proceeding with call');
      }

      // Make emergency call
      await this.showToast('Placing emergency call...');
      await this.callNumber.callNumber(this.emergencyContact, true);
      
    } catch (error) {
      console.error('Emergency trigger error:', error);
      await this.showToast('Emergency action failed. Please try again or call emergency services directly.');
    }
  }

  private async showToast(message: string): Promise<void> {
    try {
      await Toast.show({
        text: message,
        duration: 'short',
        position: 'bottom'
      });
    } catch (error) {
      console.error('Toast error:', error);
    }
  }
}