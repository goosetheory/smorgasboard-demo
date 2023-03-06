import { Component, OnInit, ChangeDetectorRef, NgZone } from '@angular/core';

import { ActivatedRoute } from '@angular/router';
import { Auth, Hub } from 'aws-amplify';

@Component({
	selector: 'app-navigation-bar',
	templateUrl: './navigation-bar.component.html',
	styleUrls: ['./navigation-bar.component.scss']
})
export class NavigationBarComponent implements OnInit {
	userIsLoggedIn: boolean

	constructor(public route: ActivatedRoute,
	            private cdRef: ChangeDetectorRef,
	            private ngZone: NgZone) {
	}

	ngOnInit(): void {
		Auth.currentSession().then(user => {
			this.userIsLoggedIn = true;
		})
		.catch(err => {
			this.userIsLoggedIn = false;
		});

		Hub.listen('auth', this.handleAuthEvent);
	}


	private handleAuthEvent = (data) => {
		this.ngZone.run(() => {
			switch (data.payload.event) {
				case 'signIn':
				case 'signUp':
					this.userIsLoggedIn = true;
					break;
				case 'signOut':
					this.userIsLoggedIn = false;
					break;
			}

			this.cdRef.detectChanges();
		});
	}
}
