// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'Antigravity AI Memory',
			social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/phamphunguyenhung/antigravity-self-learning' }], // Updated to point to user's expected location
			sidebar: [
				{
					label: 'Expert FAQ',
					slug: 'faq',
				},
				{
					label: 'Memory Core / Skills',
					autogenerate: { directory: 'memory' },
				},
			],
		}),
	],
});
