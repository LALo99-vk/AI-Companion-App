import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouteReuseStrategy } from '@angular/router';

import { IonicModule, IonicRouteStrategy } from '@ionic/angular';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { AngularFireModule } from '@angular/fire/compat';
import { AngularFireAuthModule } from '@angular/fire/compat/auth';

import { environment } from '../environments/environment';

import { EmergencyPage } from './emergency/emergency.page';
import { CallNumber } from '@ionic-native/call-number/ngx';
import { EmergencyPageModule } from './emergency/emergency.module';

import { HttpClient, HttpClientModule,HTTP_INTERCEPTORS, withInterceptorsFromDi, provideHttpClient } from '@angular/common/http';


@NgModule({
  declarations: [AppComponent,],
  imports: [BrowserModule, 
    IonicModule.forRoot(), 
    AppRoutingModule,
    AngularFireModule.initializeApp(environment.firebaseConfig),
    AngularFireAuthModule,
    EmergencyPageModule,
    HttpClientModule
  ],
  providers: [{ provide: RouteReuseStrategy, useClass: IonicRouteStrategy,},CallNumber,provideHttpClient(withInterceptorsFromDi())],
  bootstrap: [AppComponent,],
})
export class AppModule {}
