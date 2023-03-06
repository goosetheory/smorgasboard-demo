import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { QRCodeModule } from 'angularx-qrcode';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgxGoogleAnalyticsModule, NgxGoogleAnalyticsRouterModule } from 'ngx-google-analytics';
import { environment } from '../environments/environment';

import { AmplifyUIAngularModule } from '@aws-amplify/ui-angular';
import Amplify from 'aws-amplify';
import awsconfig from '../aws-exports'

// Fontawesome configuration
import { FontAwesomeModule, FaIconLibrary, FaConfig } from '@fortawesome/angular-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { far } from '@fortawesome/free-regular-svg-icons';
import { fab } from '@fortawesome/free-brands-svg-icons';

// Stripe configuration
import { NgxStripeModule } from 'ngx-stripe';

import { AddPhotoComponent } from './add-photo/add-photo.component';
import { AddPhotoRetryComponent } from './add-photo-retry/add-photo-retry.component';
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { ArchiveComponent } from './archive/archive.component';
import { BoardCanvasComponent } from './board/board-canvas/board-canvas.component';
import { BoardComponent } from './board/board.component';
import { BoardCreatedModalComponent } from './board-created-modal/board-created-modal.component';
import { BoardInstructionsComponent } from './board/board-instructions/board-instructions.component';
import { BoardPhotoComponent } from './board/board-photo/board-photo.component';
import { BoardStartModalComponent } from './board/board-start-modal/board-start-modal.component';
import { BoardsComponent } from './boards/boards.component';
import { ContactUsComponent } from './contact-us/contact-us.component';
import { CookiesPolicyComponent } from './cookies-policy/cookies-policy.component';
import { CreateBoardComponent } from './create-board/create-board.component';
import { FaqComponent } from './faq/faq.component';
import { FooterComponent } from './footer/footer.component';
import { FourOhFourComponent } from './four-oh-four/four-oh-four.component';
import { GetStartedComponent } from './get-started/get-started.component';
import { HomepageBannerComponent } from './homepage-banner/homepage-banner.component';
import { HomepageCallToActionComponent } from './homepage-call-to-action/homepage-call-to-action.component';
import { HomepageCardsComponent } from './homepage-cards/homepage-cards.component';
import { HomepageComponent } from './homepage/homepage.component';
import { HomepageDemoComponent } from './homepage-demo/homepage-demo.component';
import { HomepageHowItWorksComponent } from './homepage-how-it-works/homepage-how-it-works.component';
import { JoinBoardComponent } from './join-board/join-board.component';
import { LoginComponent } from './login/login.component';
import { LoveToScanComponent } from './love-to-scan/love-to-scan.component';
import { MailchimpComponent } from './footer/mailchimp/mailchimp.component';
import { NavigationBarComponent } from './navigation-bar/navigation-bar.component';
import { PrivacyPolicyComponent } from './privacy-policy/privacy-policy.component';
import { QrCodeComponent } from './board/qr-code/qr-code.component';
import { TermsOfServiceComponent } from './terms-of-service/terms-of-service.component';
import { CheckoutComponent } from './checkout/checkout.component';
import { ToastComponent } from './toast/toast.component';
import { HomepageUsesComponent } from './homepage-uses/homepage-uses.component';
import { PageBannerComponent } from './page-banner/page-banner.component';
import { PostsComponent } from './blog/posts/posts.component';
import { PostComponent } from './blog/post/post.component';
import { AllPhotosComponent } from './all-photos/all-photos.component';
import { PhotoThumbnailComponent } from './all-photos/photo-thumbnail/photo-thumbnail.component';
import { PhotoModalComponent } from './all-photos/photo-modal/photo-modal.component';
import { CanvasAlertComponent } from './board/canvas-alert/canvas-alert.component';
import { BoardTrialInfoComponent } from './board/board-trial-info/board-trial-info.component';

Amplify.configure(awsconfig);

@NgModule({
	declarations: [
	AppComponent,
	LoginComponent,
	BoardComponent,
	AddPhotoComponent,
	BoardPhotoComponent,
	BoardCanvasComponent,
	QrCodeComponent,
	JoinBoardComponent,
	NavigationBarComponent,
	BoardCreatedModalComponent,
	BoardInstructionsComponent,
	AddPhotoRetryComponent,
	HomepageComponent,
	HomepageBannerComponent,
	HomepageDemoComponent,
	HomepageCardsComponent,
	HomepageCallToActionComponent,
	FaqComponent,
	FooterComponent,
	MailchimpComponent,
	LoveToScanComponent,
	HomepageHowItWorksComponent,
	ContactUsComponent,
	PrivacyPolicyComponent,
	GetStartedComponent,
	TermsOfServiceComponent,
	CookiesPolicyComponent,
	BoardStartModalComponent,
	ArchiveComponent,
	FourOhFourComponent,
	BoardsComponent,
	CreateBoardComponent,
	CheckoutComponent,
 ToastComponent,
 HomepageUsesComponent,
 PageBannerComponent,
 PostsComponent,
 PostComponent,
 AllPhotosComponent,
 PhotoThumbnailComponent,
 PhotoModalComponent,
 CanvasAlertComponent,
 BoardTrialInfoComponent
	],
	imports: [
	AmplifyUIAngularModule,
	AppRoutingModule,
	BrowserModule,
	BrowserAnimationsModule,
	FormsModule,
	HttpClientModule,
	ReactiveFormsModule,
	QRCodeModule,
	NgbModule,
	FontAwesomeModule,
	NgxGoogleAnalyticsModule.forRoot(environment.googleAnalyticsID),
	NgxGoogleAnalyticsRouterModule,
	NgxStripeModule.forRoot(environment.stripeKey),
	],
	providers: [],
	bootstrap: [AppComponent]
})
export class AppModule {
	constructor(faConfig: FaConfig, library: FaIconLibrary) {
		faConfig.defaultPrefix = 'fas';
		library.addIconPacks(fas, far, fab);
	}
}