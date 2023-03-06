import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Auth } from 'aws-amplify';

@Injectable()
export class AuthGuard implements CanActivate {
	constructor(private router: Router) { }

	canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Promise<boolean> {
		// currentAuthenticatedUser throws an error if there is no user logged in
		return Auth.currentAuthenticatedUser()
		.then(currentUser => {
			return true;
		})
		.catch(error => {
			// not logged in so redirect to login page with the return url and return false
			let baseUrl = state.url.split('?')[0];
			this.router.navigate(['login'], { state: { redirectUrl: baseUrl, redirectParams: route.queryParams }});
			return false;
		});
	}
}