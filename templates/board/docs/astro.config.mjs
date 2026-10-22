// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// {{BOARD_TITLE}} documentation site (DropOut Hardware Handbook, chapter 08).
// Published from main by .github/workflows/docs.yml to https://karltbowers.github.io/{{BOARD}}-hw/
export default defineConfig({
	site: 'https://karltbowers.github.io',
	base: '/{{BOARD}}-hw',
	trailingSlash: 'always',
	integrations: [
		starlight({
			title: '{{BOARD_TITLE}}',
			description: '{{DESCRIPTION}}',
			social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/karlTbowers/{{BOARD}}-hw' }],
			editLink: { baseUrl: 'https://github.com/karlTbowers/{{BOARD}}-hw/edit/main/docs/' },
			lastUpdated: true,
			customCss: ['./src/styles/custom.css'],
			sidebar: [
				{ label: 'Decision overview', link: '/' },
				{ label: 'Purpose & design basis', slug: 'requirements' },
				{ label: 'System architecture', slug: 'system' },
				// One page per subsystem in src/content/docs/subsystems/; list them explicitly
				// once they exist to control the order.
				{ label: 'Subsystems', items: [{ autogenerate: { directory: 'subsystems' } }] },
				{ label: 'Decisions', slug: 'decisions' },
				{ label: 'Component baseline', slug: 'components' },
				{ label: 'Schematic interfaces', slug: 'interfaces' },
				{ label: 'Verification gates', slug: 'verification' },
				{ label: 'Source register', slug: 'sources' },
				{ label: 'Revisions', slug: 'revisions' },
			],
		}),
	],
});
