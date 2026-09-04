import { useRef, useState, type ButtonHTMLAttributes, type ChangeEvent, type FormEvent, type ReactNode } from 'react';
import { Link, Router as WouterRouter, useLocation } from 'wouter';
import {
  ArrowUpRight,
  Bell,
  BookOpen,
  Bot,
  Braces,
  Check,
  ChevronDown,
  ChevronRight,
  CircleCheck,
  Clock3,
  Copy,
  Database,
  Download,
  FileArchive,
  FileCheck2,
  FileText,
  FileUp,
  FolderOpen,
  Highlighter,
  Home,
  Layers3,
  ListFilter,
  Menu,
  MessageCircle,
  MoreHorizontal,
  Play,
  Plus,
  Quote,
  RotateCcw,
  Search,
  Send,
  Settings,
  ShieldCheck,
  SlidersHorizontal,
  Sparkles,
  Table2,
  UploadCloud,
  X,
  Zap,
  type LucideIcon,
} from 'lucide-react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ErrorBoundary } from '@/components/error-boundary';
import { Toaster } from '@/components/ui/toaster';
import { TooltipProvider } from '@/components/ui/tooltip';
import NotFound from '@/pages/not-found';

type DocType = 'pdf' | 'docx' | 'txt' | 'md';
type DocumentItem = {
  id: string;
  name: string;
  type: DocType;
  size: string;
  updated: string;
  words: string;
  pages: string;
  tag: string;
  description: string;
};
type Citation = { source: string; page: string; quote: string; confidence: string };
type ChatMessage = { id: string; role: 'user' | 'assistant'; text: string; citations?: Citation[] };

const queryClient = new QueryClient();

const initialDocuments: DocumentItem[] = [
  {
    id: 'atlas',
    name: 'Atlas product brief',
    type: 'pdf',
    size: '2.4 MB',
    updated: 'Today, 9:42 AM',
    words: '8,214',
    pages: '18',
    tag: 'Product',
    description: 'Positioning, audience notes, launch narrative, and the product principles behind Atlas.',
  },
  {
    id: 'field-notes',
    name: 'Field notes — customer calls',
    type: 'docx',
    size: '864 KB',
    updated: 'Yesterday',
    words: '12,908',
    pages: '24',
    tag: 'Research',
    description: 'Qualitative notes from 14 conversations with operations and research teams.',
  },
  {
    id: 'security',
    name: 'Security & privacy overview',
    type: 'pdf',
    size: '1.1 MB',
    updated: 'May 18, 2024',
    words: '4,672',
    pages: '11',
    tag: 'Trust',
    description: 'Data handling, retention, access controls, and the security model in plain language.',
  },
  {
    id: 'api',
    name: 'API reference v2',
    type: 'md',
    size: '76 KB',
    updated: 'May 16, 2024',
    words: '6,380',
    pages: '—',
    tag: 'Technical',
    description: 'Endpoints, authentication, webhooks, and examples for the public API.',
  },
  {
    id: 'brand',
    name: 'Brand voice guidelines',
    type: 'txt',
    size: '32 KB',
    updated: 'May 12, 2024',
    words: '1,944',
    pages: '—',
    tag: 'Brand',
    description: 'A practical guide to writing with clarity, warmth, and a point of view.',
  },
];

const navItems: { href: string; label: string; icon: LucideIcon }[] = [
  { href: '/', label: 'Overview', icon: Home },
  { href: '/chat', label: 'Ask DocuMind', icon: MessageCircle },
  { href: '/documents', label: 'Documents', icon: FolderOpen },
  { href: '/summarize', label: 'Summarize', icon: Highlighter },
  { href: '/extract', label: 'Extract fields', icon: Braces },
];

function IconForType({ type }: { type: DocType }) {
  return <FileText size={17} strokeWidth={1.8} />;
}

function DocIcon({ type }: { type: DocType }) {
  return (
    <div className="dm-doc-icon" data-type={type} aria-hidden="true">
      <IconForType type={type} />
    </div>
  );
}

function Button({
  children,
  className = '',
  variant = 'primary',
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'lime' | 'ghost' }) {
  return (
    <button
      className={`dm-btn px-3.5 py-2.5 ${variant === 'primary' ? 'dm-btn-primary' : variant === 'lime' ? 'dm-btn-lime' : 'dm-btn-ghost'} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}

function Avatar({ initials = 'MT', small = false }: { initials?: string; small?: boolean }) {
  return (
    <div
      data-testid="avatar-user"
      className={`grid shrink-0 place-items-center rounded-full bg-[#ff745d] font-bold text-[#17243a] ${small ? 'h-7 w-7 text-[10px]' : 'h-9 w-9 text-xs'}`}
    >
      {initials}
    </div>
  );
}

function Sidebar({
  open,
  onClose,
  onUpload,
}: {
  open: boolean;
  onClose: () => void;
  onUpload: () => void;
}) {
  const [location] = useLocation();
  return (
    <>
      {open && <div className="dm-sidebar-scrim md:hidden" onClick={onClose} />}
      <aside className="dm-sidebar flex min-h-[100dvh] shrink-0 flex-col px-4 py-5" data-open={open}>
        <div className="mb-10 flex items-center justify-between px-2">
          <Link href="/" data-testid="link-brand" className="flex items-center gap-3">
            <span className="dm-brand-mark"><Bot size={19} strokeWidth={2.4} /></span>
            <span className="font-semibold tracking-[-.03em] text-[17px]">DocuMind</span>
          </Link>
          <button onClick={onClose} className="rounded-lg p-1.5 text-[#b8c1c3] hover:bg-white/10 md:hidden" data-testid="button-close-sidebar">
            <X size={18} />
          </button>
        </div>
        <div className="mb-3 px-3 font-mono text-[10px] uppercase tracking-[.14em] text-[#849096]">Workspace</div>
        <nav className="space-y-1" aria-label="Main navigation">
          {navItems.map((item) => {
            const active = location === item.href;
            const Icon = item.icon;
            return (
              <Link
                href={item.href}
                key={item.href}
                onClick={onClose}
                data-testid={`link-nav-${item.label.toLowerCase().replaceAll(' ', '-')}`}
                className={`dm-sidebar-link flex items-center gap-3 rounded-xl px-3 py-2.5 text-[13px] font-medium ${active ? 'bg-[#d7f36b] text-[#17243a]' : 'text-[#bfc8c9] hover:bg-white/[.08] hover:text-[#f5f1e7]'}`}
              >
                <Icon size={17} strokeWidth={active ? 2.2 : 1.8} />
                <span>{item.label}</span>
                {item.href === '/chat' && <span className={`ml-auto h-1.5 w-1.5 rounded-full ${active ? 'bg-[#ff745d]' : 'bg-[#d7f36b]'}`} />}
              </Link>
            );
          })}
        </nav>
        <div className="mt-9 mb-3 px-3 font-mono text-[10px] uppercase tracking-[.14em] text-[#849096]">Workspace tools</div>
        <div className="space-y-1">
          <Link href="/settings" onClick={onClose} data-testid="link-nav-settings" className={`dm-sidebar-link flex items-center gap-3 rounded-xl px-3 py-2.5 text-[13px] font-medium ${location === '/settings' ? 'bg-white/10 text-[#d7f36b]' : 'text-[#bfc8c9] hover:bg-white/[.08] hover:text-[#f5f1e7]'}`}>
            <Settings size={17} strokeWidth={1.8} /><span>Settings</span>
          </Link>
          <button onClick={() => { onUpload(); onClose(); }} data-testid="button-sidebar-upload" className="dm-sidebar-link flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left text-[13px] font-medium text-[#bfc8c9] hover:bg-white/[.08] hover:text-[#f5f1e7]">
            <Plus size={17} strokeWidth={1.8} /><span>Add documents</span>
          </button>
        </div>
        <div className="mt-auto">
          <div className="mb-5 rounded-2xl border border-white/10 bg-white/[.06] p-4">
            <div className="mb-3 flex items-center justify-between">
              <span className="font-mono text-[10px] uppercase tracking-[.1em] text-[#aab5b4]">Index health</span>
              <CircleCheck size={15} className="text-[#d7f36b]" />
            </div>
            <div className="mb-2 flex items-end justify-between"><span className="text-2xl font-semibold tracking-[-.05em] text-[#f5f1e7]">98.6%</span><span className="text-[10px] text-[#aab5b4]">ready</span></div>
            <div className="h-1.5 overflow-hidden rounded-full bg-white/10"><div className="h-full w-[98.6%] rounded-full bg-[#d7f36b]" /></div>
            <p className="mt-3 text-[11px] leading-relaxed text-[#aab5b4]">All 5 sources are searchable and cited.</p>
          </div>
          <div className="flex items-center gap-3 border-t border-white/10 px-2 pt-4">
            <Avatar small initials="MT" />
            <div className="min-w-0"><div className="truncate text-xs font-semibold text-[#f5f1e7]">Maya Thompson</div><div className="truncate text-[11px] text-[#8f9a9f]">Personal workspace</div></div>
            <button className="ml-auto text-[#8f9a9f] hover:text-white" data-testid="button-account-menu"><MoreHorizontal size={17} /></button>
          </div>
        </div>
      </aside>
    </>
  );
}

function Topbar({ onMenu, search, setSearch }: { onMenu: () => void; search: string; setSearch: (value: string) => void }) {
  return (
    <header className="dm-topbar sticky top-0 z-20 flex items-center justify-between gap-4 px-4 sm:px-7">
      <div className="flex min-w-0 items-center gap-3">
        <button onClick={onMenu} className="rounded-lg p-2 text-[#536174] hover:bg-[#eeece3] md:hidden" data-testid="button-open-sidebar"><Menu size={20} /></button>
        <div className="hidden items-center gap-2 text-xs text-[#87909b] sm:flex"><span>Workspace</span><ChevronRight size={13} /><span className="font-medium text-[#25334a]">Product intelligence</span></div>
        <div className="flex items-center gap-2 text-xs font-medium text-[#25334a] sm:hidden"><span className="h-2 w-2 rounded-full bg-[#d7f36b]" /> Product intelligence</div>
      </div>
      <div className="flex items-center gap-2 sm:gap-4">
        <label className="relative hidden sm:block">
          <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#83909c]" />
          <input value={search} onChange={(event) => setSearch(event.target.value)} data-testid="input-global-search" className="dm-field h-9 w-[200px] pl-9 pr-3 text-xs" placeholder="Search workspace..." />
          <span className="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2 rounded border border-[#d8d7cf] px-1 font-mono text-[9px] text-[#98a0a6]">⌘ K</span>
        </label>
        <button className="rounded-lg p-2 text-[#657182] hover:bg-[#eeece3]" data-testid="button-notifications"><Bell size={18} strokeWidth={1.8} /></button>
        <Avatar />
      </div>
    </header>
  );
}

function PageHeader({ eyebrow, title, description, action }: { eyebrow: string; title: string; description?: string; action?: ReactNode }) {
  return (
    <div className="mb-9 flex flex-wrap items-end justify-between gap-5">
      <div>
        <div className="dm-eyebrow mb-3">{eyebrow}</div>
        <h1 className="dm-display text-[42px] font-semibold leading-[.98] text-[#17243a]" data-testid={`heading-${title.toLowerCase().replaceAll(' ', '-')}`}>{title}</h1>
        {description && <p className="mt-3 max-w-xl text-sm leading-relaxed text-[#718094]">{description}</p>}
      </div>
      {action}
    </div>
  );
}

function DocumentRow({ doc, selected, onSelect, onOpen }: { doc: DocumentItem; selected: boolean; onSelect: () => void; onOpen?: () => void }) {
  return (
    <div className={`group flex items-center gap-3 border-b border-[#e7e4dc] px-4 py-3.5 transition-colors last:border-b-0 ${selected ? 'bg-[#f0f4d9]' : 'hover:bg-[#faf9f4]'}`} data-testid={`row-document-${doc.id}`}>
      <button onClick={onSelect} className="flex min-w-0 flex-1 items-center gap-3 text-left" data-testid={`button-select-document-${doc.id}`}>
        <DocIcon type={doc.type} />
        <span className="min-w-0"><span className="block truncate text-[13px] font-semibold text-[#25334a]">{doc.name}</span><span className="mt-0.5 block text-[11px] text-[#85909b]">{doc.type.toUpperCase()} · {doc.size} · {doc.updated}</span></span>
      </button>
      <span className="hidden rounded-full bg-[#e7f1c2] px-2 py-1 font-mono text-[9px] font-semibold uppercase tracking-[.08em] text-[#61711c] sm:block">{doc.tag}</span>
      <button onClick={onOpen ?? onSelect} className="rounded-lg p-2 text-[#a2a9ac] opacity-0 transition-opacity hover:bg-[#eeece3] hover:text-[#17243a] group-hover:opacity-100 focus:opacity-100" data-testid={`button-open-document-${doc.id}`}><ArrowUpRight size={16} /></button>
    </div>
  );
}

function EmptySearch({ search, clear }: { search: string; clear: () => void }) {
  return (
    <div className="flex min-h-[220px] flex-col items-center justify-center px-5 text-center">
      <Search size={24} className="mb-3 text-[#9aa3a8]" />
      <h3 className="font-semibold text-[#25334a]">No matches for “{search}”</h3>
      <p className="mt-1 text-xs text-[#7e8995]">Try a document name, type, or topic.</p>
      <button onClick={clear} className="mt-4 text-xs font-semibold text-[#61711c] underline underline-offset-4" data-testid="button-clear-search">Clear search</button>
    </div>
  );
}

function Overview({ docs, search, onSearchClear, onUpload, onSelect, onAsk }: { docs: DocumentItem[]; search: string; onSearchClear: () => void; onUpload: () => void; onSelect: (id: string) => void; onAsk: () => void }) {
  const filtered = docs.filter((doc) => `${doc.name} ${doc.type} ${doc.tag}`.toLowerCase().includes(search.toLowerCase()));
  return (
    <div className="dm-page dm-stagger">
      <PageHeader eyebrow="Tuesday, June 04, 2024" title="Good morning, Maya." description="Your knowledge base is clear, current, and ready for a better question." action={<Button onClick={onUpload} variant="lime" data-testid="button-upload-header"><UploadCloud size={16} /> Add documents</Button>} />
      <div className="mb-8 grid gap-4 sm:grid-cols-3">
        {[
          { label: 'Indexed sources', value: '05', note: 'all searchable', icon: Database, color: 'bg-[#e8f1c8]' },
          { label: 'Words in workspace', value: '34.1k', note: '+2.8k this week', icon: Layers3, color: 'bg-[#ffe2dc]' },
          { label: 'Answers this month', value: '47', note: 'with citations', icon: Sparkles, color: 'bg-[#dbeee9]' },
        ].map((stat) => { const Icon = stat.icon; return <div className="dm-card dm-card-hover flex items-start justify-between p-5" key={stat.label} data-testid={`stat-${stat.label.toLowerCase().replaceAll(' ', '-')}`}><div><div className="dm-eyebrow mb-4">{stat.label}</div><div className="dm-display text-3xl font-semibold text-[#17243a]">{stat.value}</div><div className="mt-1 text-[11px] text-[#75818e]">{stat.note}</div></div><div className={`grid h-9 w-9 place-items-center rounded-xl ${stat.color} text-[#25334a]`}><Icon size={17} /></div></div>; })}
      </div>
      <div className="grid gap-5 lg:grid-cols-[1.45fr_.85fr]">
        <section className="dm-card overflow-hidden" data-testid="section-recent-documents">
          <div className="flex items-center justify-between border-b border-[#e7e4dc] px-5 py-4"><div><h2 className="text-sm font-bold text-[#25334a]">Recent documents</h2><p className="mt-1 text-[11px] text-[#87919c]">Your most recently touched sources</p></div><Link href="/documents" data-testid="link-view-all-documents" className="flex items-center gap-1 text-xs font-bold text-[#61711c] hover:text-[#17243a]">View all <ChevronRight size={14} /></Link></div>
          {filtered.length ? filtered.slice(0, 4).map((doc) => <DocumentRow key={doc.id} doc={doc} selected={false} onSelect={() => onSelect(doc.id)} onOpen={() => onSelect(doc.id)} />) : <EmptySearch search={search} clear={onSearchClear} />}
        </section>
        <section className="relative overflow-hidden rounded-2xl bg-[#17243a] p-6 text-[#f5f1e7]" data-testid="card-ask-documind">
          <div className="absolute -right-12 -top-14 h-40 w-40 rounded-full border-[24px] border-[#d7f36b]/20" />
          <div className="absolute -bottom-10 -left-5 h-28 w-28 rounded-full bg-[#ff745d]/80 blur-[1px]" />
          <div className="relative"><div className="mb-12 flex items-center justify-between"><span className="grid h-9 w-9 place-items-center rounded-xl bg-[#d7f36b] text-[#17243a]"><Bot size={18} /></span><span className="rounded-full border border-white/15 px-2.5 py-1 font-mono text-[9px] uppercase tracking-[.12em] text-[#b8c3c0]">Online</span></div><h2 className="dm-display max-w-[230px] text-[30px] font-semibold leading-[.98]">Start with the messy question.</h2><p className="mt-3 max-w-[245px] text-xs leading-relaxed text-[#aeb9b9]">I’ll trace the answer back to the exact words in your sources.</p><button onClick={onAsk} className="mt-7 flex items-center gap-2 text-xs font-bold text-[#d7f36b] hover:text-white" data-testid="button-ask-documind">Open a new thread <ArrowUpRight size={15} /></button></div>
        </section>
      </div>
      <section className="mt-5 grid gap-5 lg:grid-cols-[.8fr_1.2fr]">
        <div className="dm-card p-5" data-testid="card-index-activity"><div className="mb-5 flex items-center justify-between"><div><h2 className="text-sm font-bold text-[#25334a]">Index activity</h2><p className="mt-1 text-[11px] text-[#87919c]">Last 7 days</p></div><span className="rounded-full bg-[#e7f1c2] px-2 py-1 font-mono text-[9px] font-semibold text-[#61711c]">+12%</span></div><div className="flex h-[90px] items-end gap-2">{[26, 42, 34, 58, 46, 72, 64, 84, 77, 91, 75, 96, 88, 100].map((height, index) => <div key={index} className="group flex flex-1 flex-col items-center gap-1"><div className={`w-full rounded-[3px] ${index > 10 ? 'bg-[#17243a]' : 'bg-[#c8d7a0]'} transition-all group-hover:bg-[#ff745d]`} style={{ height: `${height}%` }} /><span className="text-[8px] text-[#a0a6a7]">{index % 2 === 0 ? ['M','T','W','T','F','S','S'][index / 2] : ''}</span></div>)}</div></div>
        <div className="dm-card flex flex-col justify-between p-5" data-testid="card-workspace-tip"><div className="flex items-center gap-2 text-[#61711c]"><Zap size={16} /><span className="dm-eyebrow !text-[#61711c]">A useful shortcut</span></div><div className="mt-6 flex flex-wrap items-end justify-between gap-4"><div><h2 className="dm-display text-2xl font-semibold text-[#25334a]">Answers get better when sources get specific.</h2><p className="mt-2 max-w-md text-xs leading-relaxed text-[#75818e]">Try asking for a comparison, a quote, or a decision. DocuMind will show its working.</p></div><Link href="/chat" data-testid="link-try-a-question" className="dm-btn dm-btn-ghost px-3.5 py-2.5 text-xs">Try a question <ArrowUpRight size={15} /></Link></div></div>
      </section>
    </div>
  );
}

function ChatView({ docs, selectedDocId, onSelectDoc, onOpenCitation, messages, onSend, sending }: { docs: DocumentItem[]; selectedDocId: string; onSelectDoc: (id: string) => void; onOpenCitation: (citation: Citation) => void; messages: ChatMessage[]; onSend: (text: string) => void; sending: boolean }) {
  const [draft, setDraft] = useState('');
  const selected = docs.find((doc) => doc.id === selectedDocId) ?? docs[0];
  const suggestions = ['What is Atlas built to solve?', 'Summarize the customer pain points', 'How does the API authentication work?'];
  const submit = (event: FormEvent) => { event.preventDefault(); if (draft.trim()) { onSend(draft.trim()); setDraft(''); } };
  return (
    <div className="dm-page">
      <PageHeader eyebrow="Ask DocuMind" title="A thinking partner, not a search box." description="Ask in your own words. Every answer stays close to the source." action={<div className="flex items-center gap-2 rounded-full border border-[#dcdad2] bg-[#fffef9] px-3 py-2 text-[11px] text-[#687585]"><span className="h-2 w-2 rounded-full bg-[#d7f36b]" /> {docs.length} sources in context</div>} />
      <div className="grid gap-5 xl:grid-cols-[1fr_290px]">
        <section className="dm-card flex min-h-[610px] flex-col overflow-hidden" data-testid="section-chat">
          <div className="flex items-center justify-between border-b border-[#e7e4dc] px-5 py-4"><div className="flex items-center gap-3"><span className="grid h-8 w-8 place-items-center rounded-lg bg-[#e7f1c2] text-[#61711c]"><Bot size={16} /></span><div><div className="text-xs font-bold text-[#25334a]">New research thread</div><div className="font-mono text-[9px] uppercase tracking-[.08em] text-[#9aa3a8]">Cited answers on</div></div></div><button className="rounded-lg p-2 text-[#85909b] hover:bg-[#eeece3]" onClick={() => onSend('Start a fresh overview of this workspace.')} data-testid="button-new-chat"><RotateCcw size={15} /></button></div>
          <div className="dm-stagger flex-1 space-y-5 overflow-auto p-5">
            {messages.map((message) => message.role === 'assistant' ? <div key={message.id} className="flex max-w-[680px] gap-3"><span className="mt-1 grid h-7 w-7 shrink-0 place-items-center rounded-lg bg-[#17243a] text-[#d7f36b]"><Bot size={14} /></span><div className="min-w-0"><div className="dm-chat-bubble px-4 py-3.5 text-[13px] leading-[1.65] text-[#34445a]" data-testid={`message-assistant-${message.id}`}>{message.text}</div>{message.citations && <div className="mt-2 flex flex-wrap gap-2">{message.citations.map((citation, index) => <button key={citation.source} onClick={() => onOpenCitation(citation)} className="group flex items-center gap-1.5 rounded-md border border-[#dadfd0] bg-[#f4f6e6] px-2.5 py-1.5 text-left text-[10px] font-semibold text-[#61711c] transition-colors hover:border-[#b8ca67] hover:bg-[#e9efca]" data-testid={`button-citation-${message.id}-${index}`}><Quote size={11} /> {citation.source} · {citation.page}<ChevronRight size={11} className="opacity-50 transition-transform group-hover:translate-x-0.5" /></button>)}</div>}</div></div> : <div key={message.id} className="ml-auto flex max-w-[540px] justify-end"><div className="dm-chat-user px-4 py-3 text-[13px] leading-relaxed" data-testid={`message-user-${message.id}`}>{message.text}</div></div>)}
            {sending && <div className="flex gap-3"><span className="grid h-7 w-7 shrink-0 place-items-center rounded-lg bg-[#17243a] text-[#d7f36b]"><Bot size={14} /></span><div className="dm-chat-bubble flex items-center gap-1 px-4 py-4"><span className="h-1.5 w-1.5 animate-pulse rounded-full bg-[#879492]" /><span className="h-1.5 w-1.5 animate-pulse rounded-full bg-[#879492] [animation-delay:150ms]" /><span className="h-1.5 w-1.5 animate-pulse rounded-full bg-[#879492] [animation-delay:300ms]" /></div></div>}
          </div>
          <div className="border-t border-[#e7e4dc] p-4"><div className="mb-3 flex flex-wrap gap-2">{suggestions.map((suggestion) => <button key={suggestion} onClick={() => setDraft(suggestion)} className="rounded-full border border-[#deddd4] px-2.5 py-1.5 text-[10px] font-medium text-[#6d7a88] transition-colors hover:border-[#aebb6c] hover:bg-[#f0f4d9]" data-testid={`button-suggestion-${suggestion.slice(0, 12).replaceAll(' ', '-').toLowerCase()}`}>{suggestion}</button>)}</div><form onSubmit={submit} className="relative"><textarea value={draft} onChange={(event) => setDraft(event.target.value)} data-testid="input-chat-prompt" className="dm-field min-h-[72px] resize-none py-3 pl-3.5 pr-14 text-sm" placeholder="Ask anything about your sources..." /><button type="submit" disabled={!draft.trim() || sending} data-testid="button-send-chat" className="absolute bottom-2.5 right-2.5 grid h-9 w-9 place-items-center rounded-lg bg-[#d7f36b] text-[#17243a] transition-all hover:bg-[#c4e457] disabled:cursor-not-allowed disabled:opacity-40"><Send size={16} /></button></form><div className="mt-2 flex items-center gap-1.5 text-[10px] text-[#99a1a6]"><ShieldCheck size={12} /> Answers are grounded in your workspace sources</div></div>
        </section>
        <aside className="dm-card h-fit p-4" data-testid="card-chat-context"><div className="mb-4 flex items-center justify-between"><div><div className="dm-eyebrow mb-1">In context</div><h2 className="text-sm font-bold text-[#25334a]">Source focus</h2></div><button className="rounded-lg p-2 text-[#8b969d] hover:bg-[#eeece3]" data-testid="button-filter-context"><SlidersHorizontal size={15} /></button></div><div className="mb-3 rounded-xl bg-[#f0f4d9] p-3"><div className="mb-2 flex items-center gap-2"><DocIcon type={selected.type} /><span className="min-w-0 truncate text-xs font-semibold text-[#25334a]">{selected.name}</span></div><p className="text-[11px] leading-relaxed text-[#73808c]">{selected.description}</p></div><div className="space-y-1">{docs.slice(0, 4).map((doc) => <button key={doc.id} onClick={() => onSelectDoc(doc.id)} data-testid={`button-context-${doc.id}`} className={`flex w-full items-center gap-2 rounded-lg px-2 py-2 text-left text-[11px] transition-colors ${doc.id === selected.id ? 'bg-[#eeece3] font-semibold text-[#25334a]' : 'text-[#7a8792] hover:bg-[#faf9f4]'}`}><span className={`h-1.5 w-1.5 rounded-full ${doc.id === selected.id ? 'bg-[#ff745d]' : 'bg-[#c5cec1]'}`} /><span className="truncate">{doc.name}</span>{doc.id === selected.id && <Check size={13} className="ml-auto text-[#61711c]" />}</button>)}</div><Link href="/documents" data-testid="link-manage-context" className="mt-4 flex items-center justify-center gap-1 border-t border-[#e7e4dc] pt-4 text-[11px] font-bold text-[#61711c]">Manage sources <ArrowUpRight size={13} /></Link></aside>
      </div>
    </div>
  );
}

function DocumentsView({ docs, search, setSearch, selectedDocId, onSelect, onUpload }: { docs: DocumentItem[]; search: string; setSearch: (value: string) => void; selectedDocId: string; onSelect: (id: string) => void; onUpload: () => void }) {
  const [filter, setFilter] = useState<'All' | DocType>('All');
  const filtered = docs.filter((doc) => (filter === 'All' || doc.type === filter) && `${doc.name} ${doc.tag}`.toLowerCase().includes(search.toLowerCase()));
  return (
    <div className="dm-page">
      <PageHeader eyebrow="Knowledge base" title="Your source shelf." description="A living index of the files DocuMind can read, connect, and cite." action={<Button onClick={onUpload} variant="lime" data-testid="button-upload-documents"><UploadCloud size={16} /> Upload files</Button>} />
      <div className="mb-5 grid gap-3 sm:grid-cols-[1fr_auto]"><label className="relative"><Search size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#88939c]" /><input value={search} onChange={(event) => setSearch(event.target.value)} data-testid="input-document-search" className="dm-field h-11 pl-10 pr-3 text-sm" placeholder="Search by name or collection..." /></label><div className="flex items-center gap-1 rounded-xl border border-[#deddd4] bg-[#fffef9] p-1">{(['All', 'pdf', 'docx', 'md', 'txt'] as const).map((item) => <button key={item} onClick={() => setFilter(item)} data-testid={`button-filter-${item}`} className={`rounded-lg px-3 py-2 text-[11px] font-bold transition-colors ${filter === item ? 'bg-[#17243a] text-[#d7f36b]' : 'text-[#7c8790] hover:bg-[#eeece3]'}`}>{item === 'All' ? 'All files' : item.toUpperCase()}</button>)}</div></div>
      <div className="dm-card overflow-hidden" data-testid="section-document-library"><div className="flex items-center justify-between border-b border-[#e7e4dc] px-5 py-4"><div className="flex items-center gap-2 text-xs font-bold text-[#25334a]"><ListFilter size={15} className="text-[#61711c]" /> {filtered.length} indexed {filtered.length === 1 ? 'source' : 'sources'}</div><div className="flex items-center gap-3 text-[10px] text-[#89939b]"><span className="hidden sm:inline">Sorted by last updated</span><button data-testid="button-sort-documents" className="rounded-md p-1 hover:bg-[#eeece3]"><ChevronDown size={14} /></button></div></div>{filtered.length ? filtered.map((doc) => <DocumentRow key={doc.id} doc={doc} selected={doc.id === selectedDocId} onSelect={() => onSelect(doc.id)} onOpen={() => onSelect(doc.id)} />) : <EmptySearch search={search} clear={() => setSearch('')} />}</div>
      <div className="mt-5 grid gap-4 sm:grid-cols-2"><div className="rounded-2xl border border-dashed border-[#c5c9ba] bg-[#f0f4d9]/55 p-5"><div className="mb-3 flex items-center justify-between"><UploadCloud size={20} className="text-[#61711c]" /><span className="font-mono text-[9px] uppercase tracking-[.12em] text-[#8b9690]">Quick add</span></div><h3 className="text-sm font-bold text-[#25334a]">Drop a source into the shelf.</h3><p className="mt-1 max-w-sm text-xs leading-relaxed text-[#78848e]">PDF, DOCX, TXT, and Markdown files are ready to be indexed.</p><button onClick={onUpload} className="mt-4 text-xs font-bold text-[#61711c] underline underline-offset-4" data-testid="button-quick-add">Choose files</button></div><div className="rounded-2xl bg-[#ff745d] p-5 text-[#17243a]"><div className="mb-5 flex items-center justify-between"><FileCheck2 size={20} /><span className="font-mono text-[9px] uppercase tracking-[.12em] opacity-60">Trust signal</span></div><h3 className="text-sm font-bold">Every answer keeps a paper trail.</h3><p className="mt-1 max-w-sm text-xs leading-relaxed text-[#553c3a]">Citations point back to a source and page, so review takes seconds—not faith.</p></div></div>
    </div>
  );
}

function SummarizeView({ docs, selectedDocId, onSelectDoc, onExport, notify }: { docs: DocumentItem[]; selectedDocId: string; onSelectDoc: (id: string) => void; onExport: (content: string, filename: string) => void; notify: (message: string) => void }) {
  const [style, setStyle] = useState('Executive brief');
  const [ran, setRan] = useState(false);
  const [running, setRunning] = useState(false);
  const selected = docs.find((doc) => doc.id === selectedDocId) ?? docs[0];
  const summary = style === 'Executive brief' ? 'Atlas is a focused workspace for turning fragmented internal knowledge into confident decisions. Its strongest promise is not faster search; it is the ability to show why an answer is trustworthy. The product is positioned for teams who already have information, but lose time finding the thread.' : style === 'Key takeaways' ? '• Turns fragmented source material into cited answers\\n• Makes trust visible through source-level evidence\\n• Built for teams with high-volume, high-context research\\n• The clearest differentiator is explainability, not retrieval speed' : 'Atlas helps research-heavy teams move from scattered information to well-supported decisions. The product combines a searchable knowledge base with answer traces, giving users a fast way to understand not only what is true, but where that truth came from.';
  const run = () => { setRunning(true); setRan(false); window.setTimeout(() => { setRunning(false); setRan(true); notify('Summary is ready to review.'); }, 650); };
  return (
    <div className="dm-page">
      <PageHeader eyebrow="Summarize a source" title="Make the long thing legible." description="Choose a style, keep the nuance, and get a clear first pass in seconds." action={<Button onClick={() => onExport(summary, `${selected.name}-summary.txt`)} variant="ghost" data-testid="button-export-summary"><Download size={15} /> Export</Button>} />
      <div className="grid gap-5 xl:grid-cols-[280px_1fr]">
        <aside className="dm-card h-fit p-4" data-testid="card-summary-controls"><div className="mb-4 flex items-center justify-between"><div><div className="dm-eyebrow mb-1">Source</div><h2 className="text-sm font-bold text-[#25334a]">Choose a document</h2></div><FileArchive size={16} className="text-[#61711c]" /></div><div className="space-y-1.5">{docs.map((doc) => <button key={doc.id} onClick={() => { onSelectDoc(doc.id); setRan(false); }} data-testid={`button-summary-source-${doc.id}`} className={`flex w-full items-center gap-2.5 rounded-xl p-2.5 text-left transition-colors ${selected.id === doc.id ? 'bg-[#f0f4d9]' : 'hover:bg-[#faf9f4]'}`}><DocIcon type={doc.type} /><span className="min-w-0"><span className="block truncate text-[11px] font-semibold text-[#34445a]">{doc.name}</span><span className="mt-0.5 block text-[10px] text-[#929ba0]">{doc.words} words</span></span>{selected.id === doc.id && <Check size={14} className="ml-auto shrink-0 text-[#61711c]" />}</button>)}</div><div className="mt-5 border-t border-[#e7e4dc] pt-4"><div className="dm-eyebrow mb-3">Summary style</div><div className="space-y-2">{['Executive brief', 'Key takeaways', 'Plain-language'].map((item) => <button key={item} onClick={() => { setStyle(item); setRan(false); }} data-testid={`button-summary-style-${item.toLowerCase().replaceAll(' ', '-')}`} className={`flex w-full items-center justify-between rounded-xl border px-3 py-2.5 text-left text-xs font-semibold transition-colors ${style === item ? 'border-[#b8ca67] bg-[#f0f4d9] text-[#25334a]' : 'border-[#e3e1d8] text-[#7b8791] hover:bg-[#faf9f4]'}`}>{item}{style === item && <CircleCheck size={15} className="text-[#61711c]" />}</button>)}</div></div><Button onClick={run} className="mt-5 w-full" variant="lime" disabled={running} data-testid="button-run-summary">{running ? <><span className="h-3 w-3 animate-spin rounded-full border-2 border-[#17243a]/30 border-t-[#17243a]" /> Reading source</> : <><Sparkles size={15} /> Generate summary</>}</Button></aside>
        <section className="dm-card min-h-[520px] overflow-hidden" data-testid="section-summary-output"><div className="flex flex-wrap items-center justify-between gap-3 border-b border-[#e7e4dc] px-6 py-4"><div className="flex items-center gap-3"><DocIcon type={selected.type} /><div><h2 className="text-sm font-bold text-[#25334a]">{selected.name}</h2><div className="mt-1 flex items-center gap-2 text-[10px] text-[#8a959d]"><span>{selected.pages} pages</span><span>·</span><span>{style}</span></div></div></div><div className={`flex items-center gap-1.5 rounded-full px-2.5 py-1 font-mono text-[9px] uppercase tracking-[.08em] ${ran ? 'bg-[#e7f1c2] text-[#61711c]' : 'bg-[#eeece3] text-[#919a9e]'}`}>{ran ? <CircleCheck size={12} /> : <Clock3 size={12} />}{ran ? 'Ready' : 'Draft'}</div></div>{ran ? <div className="dm-stagger p-6"><div className="mb-7 flex items-center justify-between border-b border-[#e7e4dc] pb-5"><div><div className="dm-eyebrow mb-2">Generated summary</div><h3 className="dm-display text-3xl font-semibold text-[#17243a]">{style}</h3></div><span className="rounded-lg bg-[#ff745d] px-2 py-1 font-mono text-[9px] font-bold uppercase tracking-[.08em] text-[#17243a]">DocuMind pass</span></div><p className="max-w-2xl whitespace-pre-line text-[15px] leading-[1.85] text-[#43536a]" data-testid="text-summary-result">{summary}</p><div className="mt-9 grid gap-3 border-t border-[#e7e4dc] pt-5 sm:grid-cols-3"><div><div className="dm-eyebrow mb-1">Source coverage</div><div className="text-sm font-bold text-[#25334a]">18 / 18 pages</div></div><div><div className="dm-eyebrow mb-1">Confidence</div><div className="text-sm font-bold text-[#25334a]">High · 94.2%</div></div><div><div className="dm-eyebrow mb-1">Generated</div><div className="text-sm font-bold text-[#25334a]">Just now</div></div></div></div> : <div className="flex min-h-[410px] flex-col items-center justify-center p-8 text-center"><div className="mb-5 grid h-14 w-14 place-items-center rounded-2xl bg-[#f0f4d9] text-[#61711c]"><Highlighter size={24} /></div><h3 className="dm-display text-2xl font-semibold text-[#25334a]">Your summary will land here.</h3><p className="mt-2 max-w-sm text-xs leading-relaxed text-[#7d8993]">Select a style that matches the moment, then let DocuMind read the source for you.</p></div>}</section>
      </div>
    </div>
  );
}

function ExtractView({ docs, selectedDocId, onSelectDoc, onExport, notify }: { docs: DocumentItem[]; selectedDocId: string; onSelectDoc: (id: string) => void; onExport: (content: string, filename: string) => void; notify: (message: string) => void }) {
  const selected = docs.find((doc) => doc.id === selectedDocId) ?? docs[0];
  const fields = ['Company / product', 'Target audience', 'Core problem', 'Differentiators', 'Pricing signal', 'Notable quote'];
  const [checked, setChecked] = useState(fields.slice(0, 4));
  const [ran, setRan] = useState(false);
  const [running, setRunning] = useState(false);
  const toggle = (field: string) => setChecked((current) => current.includes(field) ? current.filter((item) => item !== field) : [...current, field]);
  const run = () => { setRunning(true); setRan(false); window.setTimeout(() => { setRunning(false); setRan(true); notify('Fields extracted from the selected source.'); }, 700); };
  const values: Record<string, string> = { 'Company / product': 'Atlas', 'Target audience': 'Research-heavy operations teams', 'Core problem': 'Important answers are scattered across too many sources.', 'Differentiators': 'Answer traces, source-level confidence, and a calm workspace for synthesis.', 'Pricing signal': 'Team plans begin with shared workspaces and usage-based indexing.', 'Notable quote': '“Trust is a product feature, not a footnote.”' };
  const csv = checked.map((field) => `"${field}","${values[field]}"`).join('\n');
  return (
    <div className="dm-page">
      <PageHeader eyebrow="Structured output" title="Pull out the shape of an idea." description="Select the fields you care about and turn narrative source material into a useful first row." action={<Button onClick={() => onExport(csv, `${selected.name}-fields.csv`)} disabled={!ran} variant="ghost" data-testid="button-export-extract"><Download size={15} /> Export CSV</Button>} />
      <div className="grid gap-5 xl:grid-cols-[280px_1fr]">
        <aside className="dm-card h-fit p-4" data-testid="card-extract-controls"><div className="mb-4"><div className="dm-eyebrow mb-1">Source & fields</div><h2 className="text-sm font-bold text-[#25334a]">Configure extraction</h2></div><label className="dm-eyebrow mb-2 block">Document</label><select value={selected.id} onChange={(event) => { onSelectDoc(event.target.value); setRan(false); }} data-testid="select-extract-document" className="dm-field mb-5 h-10 px-3 text-xs font-semibold">{docs.map((doc) => <option key={doc.id} value={doc.id}>{doc.name}</option>)}</select><div className="mb-3 flex items-center justify-between"><label className="dm-eyebrow">Fields to extract</label><button onClick={() => setChecked(checked.length === fields.length ? [] : fields)} className="text-[10px] font-bold text-[#61711c]" data-testid="button-toggle-all-fields">{checked.length === fields.length ? 'Clear all' : 'Select all'}</button></div><div className="space-y-1">{fields.map((field) => <label key={field} className="flex cursor-pointer items-center gap-2.5 rounded-lg px-2 py-2 text-xs text-[#59697c] hover:bg-[#faf9f4]"><input type="checkbox" checked={checked.includes(field)} onChange={() => toggle(field)} data-testid={`checkbox-field-${field.toLowerCase().replaceAll(' ', '-')}`} className="h-3.5 w-3.5 accent-[#17243a]" /><span>{field}</span></label>)}</div><Button onClick={run} className="mt-5 w-full" variant="lime" disabled={running || checked.length === 0} data-testid="button-run-extraction">{running ? <><span className="h-3 w-3 animate-spin rounded-full border-2 border-[#17243a]/30 border-t-[#17243a]" /> Mapping fields</> : <><Play size={14} /> Run extraction</>}</Button></aside>
        <section className="dm-card min-h-[520px] overflow-hidden" data-testid="section-extract-output"><div className="flex flex-wrap items-center justify-between gap-3 border-b border-[#e7e4dc] px-6 py-4"><div className="flex items-center gap-3"><DocIcon type={selected.type} /><div><h2 className="text-sm font-bold text-[#25334a]">{selected.name}</h2><div className="mt-1 text-[10px] text-[#8a959d]">{checked.length} fields selected · structured preview</div></div></div><Table2 size={18} className="text-[#61711c]" /></div>{ran ? <div className="overflow-auto p-5"><div className="mb-4 flex items-center justify-between"><div className="flex items-center gap-2 text-xs font-bold text-[#25334a]"><CircleCheck size={15} className="text-[#6e8913]" /> Extraction complete</div><span className="font-mono text-[10px] text-[#90999d]">confidence weighted</span></div><div className="overflow-hidden rounded-xl border border-[#e1dfd5]"><table className="w-full min-w-[560px] border-collapse text-left"><thead><tr className="bg-[#f0f4d9] text-[10px] uppercase tracking-[.08em] text-[#68761f]"><th className="px-4 py-3 font-mono font-semibold">Field</th><th className="px-4 py-3 font-mono font-semibold">Extracted value</th><th className="px-4 py-3 text-right font-mono font-semibold">Confidence</th></tr></thead><tbody>{checked.map((field, index) => <tr key={field} className="border-t border-[#e7e4dc] text-xs text-[#43536a]" data-testid={`row-extracted-${index}`}><td className="px-4 py-3.5 font-semibold text-[#25334a]">{field}</td><td className="max-w-[360px] px-4 py-3.5">{values[field]}</td><td className="px-4 py-3.5 text-right"><span className="rounded-full bg-[#e7f1c2] px-2 py-1 font-mono text-[9px] font-semibold text-[#61711c]">{index === 4 ? '81%' : '96%'}</span></td></tr>)}</tbody></table></div></div> : <div className="flex min-h-[410px] flex-col items-center justify-center p-8 text-center"><div className="mb-5 grid h-14 w-14 place-items-center rounded-2xl bg-[#ffe2dc] text-[#bc4e3d]"><Braces size={24} /></div><h3 className="dm-display text-2xl font-semibold text-[#25334a]">A clean table from a messy page.</h3><p className="mt-2 max-w-sm text-xs leading-relaxed text-[#7d8993]">Choose your fields and run extraction to see the first structured pass.</p></div>}</section>
      </div>
    </div>
  );
}

function SettingsView({ notify }: { notify: (message: string) => void }) {
  const [settings, setSettings] = useState({ citations: true, suggestions: true, emails: false, dark: false });
  const toggle = (key: keyof typeof settings) => setSettings((current) => ({ ...current, [key]: !current[key] }));
  return (
    <div className="dm-page">
      <PageHeader eyebrow="Workspace preferences" title="Make it yours." description="A few quiet controls for how DocuMind thinks alongside you." />
      <div className="grid gap-5 lg:grid-cols-[1fr_300px]">
        <div className="space-y-5">
          <section className="dm-card overflow-hidden" data-testid="section-settings-account"><div className="border-b border-[#e7e4dc] px-5 py-4"><div className="dm-eyebrow mb-1">Profile</div><h2 className="text-sm font-bold text-[#25334a]">Your workspace identity</h2></div><div className="grid gap-4 p-5 sm:grid-cols-2"><label className="text-xs font-semibold text-[#566679]">Full name<input defaultValue="Maya Thompson" data-testid="input-settings-name" className="dm-field mt-2 h-10 px-3 text-sm font-normal" /></label><label className="text-xs font-semibold text-[#566679]">Email address<input defaultValue="maya@northstar.studio" data-testid="input-settings-email" className="dm-field mt-2 h-10 px-3 text-sm font-normal" /></label><label className="text-xs font-semibold text-[#566679] sm:col-span-2">Workspace name<input defaultValue="Product intelligence" data-testid="input-settings-workspace" className="dm-field mt-2 h-10 px-3 text-sm font-normal" /></label><div className="sm:col-span-2"><Button onClick={() => notify('Profile settings saved.')} variant="primary" data-testid="button-save-profile">Save changes</Button></div></div></section>
          <section className="dm-card overflow-hidden" data-testid="section-settings-behavior"><div className="border-b border-[#e7e4dc] px-5 py-4"><div className="dm-eyebrow mb-1">Behavior</div><h2 className="text-sm font-bold text-[#25334a]">How DocuMind shows its work</h2></div><div className="divide-y divide-[#e7e4dc]">{[{ key: 'citations' as const, icon: Quote, title: 'Always show citations', note: 'Keep source references visible beneath every answer.' }, { key: 'suggestions' as const, icon: Sparkles, title: 'Question suggestions', note: 'Offer useful next questions after an answer.' }, { key: 'emails' as const, icon: Bell, title: 'Weekly workspace digest', note: 'A short note about new and changed sources.' }].map((item) => { const Icon = item.icon; return <div key={item.key} className="flex items-center justify-between gap-4 px-5 py-4"><div className="flex items-center gap-3"><span className="grid h-8 w-8 place-items-center rounded-lg bg-[#eeece3] text-[#637184]"><Icon size={15} /></span><div><div className="text-xs font-bold text-[#34445a]">{item.title}</div><div className="mt-1 text-[11px] text-[#8b959c]">{item.note}</div></div></div><button onClick={() => toggle(item.key)} aria-pressed={settings[item.key]} data-testid={`button-toggle-${item.key}`} className={`relative h-6 w-11 rounded-full p-1 transition-colors ${settings[item.key] ? 'bg-[#17243a]' : 'bg-[#d7d9d1]'}`}><span className={`block h-4 w-4 rounded-full bg-[#f7f5ef] transition-transform ${settings[item.key] ? 'translate-x-5' : ''}`} /></button></div>; })}</div></section>
        </div>
        <aside className="space-y-5"><div className="rounded-2xl bg-[#17243a] p-5 text-[#f5f1e7]" data-testid="card-settings-plan"><div className="mb-8 flex items-center justify-between"><span className="grid h-9 w-9 place-items-center rounded-xl bg-[#d7f36b] text-[#17243a]"><Zap size={17} /></span><span className="rounded-full border border-white/15 px-2 py-1 font-mono text-[9px] uppercase tracking-[.1em] text-[#c5ceca]">Personal</span></div><div className="dm-eyebrow !text-[#9ba9a8]">Index usage</div><div className="mt-2 flex items-baseline gap-2"><span className="dm-display text-3xl font-semibold">34.1k</span><span className="text-xs text-[#a1adac]">/ 100k words</span></div><div className="dm-progress-track mt-4 bg-white/10"><div className="dm-progress-bar w-[34%]" /></div><p className="mt-4 text-[11px] leading-relaxed text-[#a1adac]">Your workspace has plenty of room for the next rabbit hole.</p><button onClick={() => notify('Plan details are coming soon.')} className="mt-5 flex items-center gap-1 text-xs font-bold text-[#d7f36b]" data-testid="button-view-plan">View plan details <ArrowUpRight size={14} /></button></div><div className="dm-card p-5" data-testid="card-settings-security"><div className="mb-4 flex items-center gap-2"><ShieldCheck size={17} className="text-[#61711c]" /><h2 className="text-sm font-bold text-[#25334a]">Privacy by default</h2></div><p className="text-xs leading-relaxed text-[#7d8993]">Your documents are private to this workspace. We never use them to train shared models.</p><button onClick={() => notify('Security settings opened.')} className="mt-4 text-xs font-bold text-[#61711c] underline underline-offset-4" data-testid="button-security-settings">Review security</button></div></aside>
      </div>
    </div>
  );
}

function CitationModal({ citation, onClose }: { citation: Citation; onClose: () => void }) {
  return <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#17243a]/35 p-4 backdrop-blur-sm" role="dialog" aria-modal="true" data-testid="modal-citation"><div className="dm-card w-full max-w-lg overflow-hidden shadow-2xl"><div className="flex items-center justify-between border-b border-[#e7e4dc] px-5 py-4"><div className="flex items-center gap-3"><span className="grid h-8 w-8 place-items-center rounded-lg bg-[#e7f1c2] text-[#61711c]"><Quote size={15} /></span><div><div className="text-xs font-bold text-[#25334a]">{citation.source}</div><div className="font-mono text-[9px] uppercase tracking-[.08em] text-[#919b9f]">{citation.page} · Citation detail</div></div></div><button onClick={onClose} className="rounded-lg p-2 text-[#7c8791] hover:bg-[#eeece3]" data-testid="button-close-citation"><X size={17} /></button></div><div className="p-6"><div className="dm-eyebrow mb-3">Source passage</div><blockquote className="border-l-2 border-[#ff745d] pl-4 text-[15px] leading-[1.7] text-[#43536a]">“{citation.quote}”</blockquote><div className="mt-7 flex items-center justify-between rounded-xl bg-[#f0f4d9] p-3.5"><div><div className="text-[11px] font-bold text-[#53621d]">Evidence confidence</div><div className="mt-1 text-[10px] text-[#7e8c51]">Based on source clarity and answer overlap</div></div><span className="font-mono text-lg font-semibold text-[#61711c]">{citation.confidence}</span></div><div className="mt-5 flex justify-end gap-2"><button onClick={() => navigator.clipboard?.writeText(citation.quote)} className="dm-btn dm-btn-ghost px-3 py-2 text-xs" data-testid="button-copy-citation"><Copy size={14} /> Copy passage</button><button onClick={onClose} className="dm-btn dm-btn-primary px-3 py-2 text-xs" data-testid="button-done-citation">Done</button></div></div></div></div>;
}

function ToastNotice({ message, onClose }: { message: string; onClose: () => void }) {
  return <div className="fixed bottom-5 right-5 z-50 flex max-w-[320px] items-center gap-3 rounded-xl bg-[#17243a] px-4 py-3 text-xs font-semibold text-[#f5f1e7] shadow-xl" data-testid="status-toast"><span className="grid h-6 w-6 place-items-center rounded-lg bg-[#d7f36b] text-[#17243a]"><Check size={14} /></span><span>{message}</span><button onClick={onClose} className="ml-1 text-[#aeb9b9] hover:text-white" data-testid="button-close-toast"><X size={14} /></button></div>;
}

function Workspace() {
  const [location, setLocation] = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [search, setSearch] = useState('');
  const [docs, setDocs] = useState(initialDocuments);
  const [selectedDocId, setSelectedDocId] = useState('atlas');
  const [messages, setMessages] = useState<ChatMessage[]>([{ id: 'welcome', role: 'assistant', text: 'I’ve read the workspace. Ask me to connect the dots, find a specific detail, or pressure-test an idea. I’ll keep the answer close to the source.', citations: [{ source: 'Atlas product brief', page: 'p. 3', quote: 'The product is designed to make the path from information to a confident decision visible.', confidence: '96%' }] }]);
  const [sending, setSending] = useState(false);
  const [citation, setCitation] = useState<Citation | null>(null);
  const [toast, setToast] = useState('');
  const uploadRef = useRef<HTMLInputElement>(null);
  const showToast = (message: string) => { setToast(message); window.setTimeout(() => setToast(''), 2800); };
  const selectDoc = (id: string) => { setSelectedDocId(id); if (location === '/') showToast('Source selected.'); };
  const handleUpload = () => uploadRef.current?.click();
  const handleFiles = (event: ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files ?? []);
    const accepted = files.filter((file) => /\.(pdf|docx|txt|md)$/i.test(file.name));
    if (accepted.length) {
      const newDocs: DocumentItem[] = accepted.map((file, index) => ({ id: `upload-${Date.now()}-${index}`, name: file.name.replace(/\.[^.]+$/, ''), type: (file.name.split('.').pop()?.toLowerCase() ?? 'txt') as DocType, size: `${Math.max(1, Math.round(file.size / 1024))} KB`, updated: 'Just now', words: 'Indexing…', pages: '—', tag: 'New source', description: 'A newly added source, ready for DocuMind to read and connect.' }));
      setDocs((current) => [...newDocs, ...current]); setSelectedDocId(newDocs[0].id); showToast(`${newDocs.length} source${newDocs.length > 1 ? 's' : ''} added to your shelf.`); setLocation('/documents');
    } else if (files.length) showToast('Choose a PDF, DOCX, TXT, or Markdown file.');
    event.target.value = '';
  };
  const sendMessage = (text: string) => {
    const userMessage: ChatMessage = { id: `user-${Date.now()}`, role: 'user', text };
    setMessages((current) => [...current, userMessage]); setSending(true);
    window.setTimeout(() => {
      const aboutPain = text.toLowerCase().includes('pain');
      const answer: ChatMessage = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        text: aboutPain
          ? 'Across the customer calls, the recurring problem is not a lack of information—it is the cost of assembling it. People describe switching between notes, docs, and conversations before they can commit to a direction. The opportunity is to make synthesis feel like a first-class workflow.'
          : 'The clearest thread is that DocuMind helps teams move from scattered source material to a decision they can stand behind. Atlas frames this as visibility into the reasoning, while the customer notes make the cost of unresolved knowledge concrete.',
        citations: aboutPain
          ? [{ source: 'Field notes — customer calls', page: 'p. 7', quote: 'I know we have the answer somewhere; I just do not know which version to trust.', confidence: '92%' }]
          : [{ source: 'Atlas product brief', page: 'p. 8', quote: 'Trust is not a review step after the answer; it is part of the answer experience.', confidence: '94%' }, { source: 'Field notes — customer calls', page: 'p. 12', quote: 'The best tool would show me the context without asking me to become a librarian.', confidence: '89%' }],
      };
      setMessages((current) => [...current, answer]);
      setSending(false);
    }, 650);
  };
  const exportFile = (content: string, filename: string) => { const blob = new Blob([content], { type: filename.endsWith('.csv') ? 'text/csv' : 'text/plain' }); const url = URL.createObjectURL(blob); const anchor = document.createElement('a'); anchor.href = url; anchor.download = filename; anchor.click(); URL.revokeObjectURL(url); showToast('Export downloaded.'); };
  const content = location === '/' ? <Overview docs={docs} search={search} onSearchClear={() => setSearch('')} onUpload={handleUpload} onSelect={selectDoc} onAsk={() => setLocation('/chat')} /> : location === '/chat' ? <ChatView docs={docs} selectedDocId={selectedDocId} onSelectDoc={selectDoc} onOpenCitation={setCitation} messages={messages} onSend={sendMessage} sending={sending} /> : location === '/documents' ? <DocumentsView docs={docs} search={search} setSearch={setSearch} selectedDocId={selectedDocId} onSelect={selectDoc} onUpload={handleUpload} /> : location === '/summarize' ? <SummarizeView docs={docs} selectedDocId={selectedDocId} onSelectDoc={selectDoc} onExport={exportFile} notify={showToast} /> : location === '/extract' ? <ExtractView docs={docs} selectedDocId={selectedDocId} onSelectDoc={selectDoc} onExport={exportFile} notify={showToast} /> : location === '/settings' ? <SettingsView notify={showToast} /> : <NotFound />;
  return <div className="dm-noise dm-shell flex"><Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} onUpload={handleUpload} /><div className="dm-main"><Topbar onMenu={() => setSidebarOpen(true)} search={search} setSearch={setSearch} />{content}</div><input ref={uploadRef} onChange={handleFiles} type="file" accept=".pdf,.docx,.txt,.md" multiple className="hidden" data-testid="input-upload-files" />{citation && <CitationModal citation={citation} onClose={() => setCitation(null)} />}{toast && <ToastNotice message={toast} onClose={() => setToast('')} />}</div>;
}

function App() {
  return <QueryClientProvider client={queryClient}><TooltipProvider><WouterRouter base={import.meta.env.BASE_URL.replace(/\/$/, '')}><ErrorBoundary><Workspace /></ErrorBoundary></WouterRouter><Toaster /></TooltipProvider></QueryClientProvider>;
}

export default App;