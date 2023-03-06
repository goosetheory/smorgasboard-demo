import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Title } from '@angular/platform-browser';

import { BlogService } from '../../services/blog.service';
import { SeoService } from '../../services/seo.service';
import { BlogPost } from '../../dtos/BlogPost';

@Component({
	selector: 'app-post',
	templateUrl: './post.component.html',
	styleUrls: ['./post.component.scss']
})
export class PostComponent implements OnInit {
	finishedLoading: boolean = false;
	post: BlogPost = null;
	noSuchPost: boolean = false;

	constructor(private route: ActivatedRoute,
	            private blogService: BlogService,
	            private titleService: Title,
	            private seoService: SeoService){}

	ngOnInit(): void {
		let slug = this.route.snapshot.params['slug'];
		this.blogService.getPost(slug)
		.then(response => {
			this.post = response;
			this.titleService.setTitle(`${this.post.title} | SmorgasBoard`);
			this.seoService.setMetaDescription(this.post.excerpt);
		})
		.catch(response => {
			this.titleService.setTitle('Blog | SmorgasBoard');
			this.noSuchPost = true;
		})
		.finally(() => {
			this.finishedLoading = true;
		});
	}
}
