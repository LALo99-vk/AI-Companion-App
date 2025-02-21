import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { EmergencyPageRoutingModule } from './emergency-routing.module';

import { EmergencyPage } from './emergency.page';

import { CallNumber } from '@ionic-native/call-number/ngx';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    EmergencyPageRoutingModule
  ],
  declarations: [EmergencyPage],
  providers:[CallNumber]
})
export class EmergencyPageModule {}
