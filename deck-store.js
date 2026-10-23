// Account + saved decks for the KazWorld word game: Google sign-in (Firebase Auth) and per-user decks (Firestore).
// Used by game.html and create-deck.html. Everything is loaded on demand, so pages that never touch accounts download nothing from Firebase.
// A deck is { id, name, words: [Kazakh words] } stored at users/{uid}/decks/{id}; firestore.rules lets a user read and write only their own.
// For automated tests a page can set window.KW_MOCK_STORE (same async methods) before this module is used; it replaces the real backend.
import { FIREBASE_CONFIG } from './firebase-config.js';

const SDK = 'https://www.gstatic.com/firebasejs/10.14.1/';
export const MAX_NAME = 40, MAX_WORDS = 200;
let real = null;

export const isConfigured = () => !!window.KW_MOCK_STORE || !!FIREBASE_CONFIG;

async function backend() {
    if (window.KW_MOCK_STORE) return window.KW_MOCK_STORE;
    if (!FIREBASE_CONFIG) throw new Error('not-configured');
    if (real) return real;
    const [appM, authM, fsM] = await Promise.all([import(SDK + 'firebase-app.js'), import(SDK + 'firebase-auth.js'), import(SDK + 'firebase-firestore.js')]);
    const app = appM.initializeApp(FIREBASE_CONFIG), auth = authM.getAuth(app), db = fsM.getFirestore(app);
    const decks = uid => fsM.collection(db, 'users', uid, 'decks');
    real = {
        // calls cb(user | null) now and on every sign-in or sign-out; user is { uid, name, email }
        onUser(cb) { return authM.onAuthStateChanged(auth, u => cb(u ? { uid: u.uid, name: u.displayName || '', email: u.email || '' } : null)); },
        async signIn() { await authM.signInWithPopup(auth, new authM.GoogleAuthProvider()); },
        async signOut() { await authM.signOut(auth); },
        async list() {
            if (!auth.currentUser) return [];
            const snap = await fsM.getDocs(fsM.query(decks(auth.currentUser.uid), fsM.orderBy('createdAt')));
            return snap.docs.map(d => ({ id: d.id, name: d.data().name, words: d.data().words || [] }));
        },
        async save(name, words) {
            if (!auth.currentUser) throw new Error('signed-out');
            const ref = await fsM.addDoc(decks(auth.currentUser.uid), { name, words, createdAt: fsM.serverTimestamp() });
            return { id: ref.id, name, words };
        },
    };
    return real;
}

export const onUser = async cb => (await backend()).onUser(cb);
export const signIn = async () => (await backend()).signIn();
export const signOutUser = async () => (await backend()).signOut();
export const listDecks = async () => (await backend()).list();

// Saves a deck for the signed-in user. Throws Error('name') for a bad name, Error('duplicate') for a name already used, Error('words') for too few or too many words.
export async function saveDeck(name, words) {
    name = String(name || '').trim();
    if (!name || name.length > MAX_NAME) throw new Error('name');
    if (!Array.isArray(words) || words.length < 5 || words.length > MAX_WORDS) throw new Error('words');
    const b = await backend();
    const existing = await b.list();
    if (existing.some(d => d.name.toLowerCase() === name.toLowerCase())) throw new Error('duplicate');
    return b.save(name, words);
}
