import { Component, OnInit, NgZone } from '@angular/core';
import { trigger, state, style, animate, transition } from '@angular/animations';

@Component({
	selector: 'app-canvas-alert',
	templateUrl: './canvas-alert.component.html',
	styleUrls: ['./canvas-alert.component.scss'],
	animations: [
	trigger('showHide', [
	        state('hide', style({ opacity: 0 })),
	        state('show', style({ opacity: 1 })),
	        transition('hide <=> show', [
	                   animate('1s 3s ease-in-out')
	                   ])])]
})
export class CanvasAlertComponent implements OnInit {
	disconnectAlertActive: boolean = false;
	reconnectAlertActive: boolean = false;
	infoAlertActive: boolean = false;
	infoMessage: string = null;

	constructor(private ngZone: NgZone) { }

	ngOnInit(): void {
	}

	public onDisconnect() {
		console.log('ca disconnect');
		this.ngZone.run(() => {

			this.disconnectAlertActive = true;
			this.reconnectAlertActive = false;
		});
	}

	public onReconnect() {
		console.log('ca reconnect');
		this.ngZone.run(() => {

			this.disconnectAlertActive = false;
			this.reconnectAlertActive = true;
		});
	}

	public showInfoAlert(message: string) {
		this.infoMessage = message;
		this.infoAlertActive = true;
	}



	public hideInfoAlert() {
		this.infoAlertActive = false;
	}
}
