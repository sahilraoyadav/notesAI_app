import './index.css';
import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import axios from 'axios';
import NoteEditor from './components/notes/NoteEditor';

const API = 'http://localhost:8000';
function App(){
  const [notes,setNotes]=useState([]); const [activeId,setActiveId]=useState(null); const [filter,setFilter]=useState('all'); const [chatQ,setChatQ]=useState(''); const [chatA,setChatA]=useState('');
  const load=async()=>{const data=(await axios.get(`${API}/notes`)).data;setNotes(data);if(data.length&&!activeId) setActiveId(data[0].id);};
  useEffect(()=>{load();},[]);
  const active=useMemo(()=>notes.find(n=>n.id===activeId),[notes,activeId]); const filtered=useMemo(()=>filter==='all'?notes:notes.filter(n=>n.status===filter),[notes,filter]);
  const create=async()=>{const created=(await axios.post(`${API}/notes`,{title:'Untitled note',content:'',note_type:'text',status:'todo'})).data;await load();setActiveId(created.id)};
  const save=async(patch)=>{if(!active) return; if(patch.local){setNotes(notes.map(n=>n.id===active.id?{...n,...patch.local}:n)); return;} await axios.put(`${API}/notes/${active.id}`, patch); await load();};
  return <div className='app-shell'><aside className='sidebar'><div className='sidebar-top'><h1>NotesAI</h1><button onClick={create}>+ New</button></div><select value={filter} onChange={e=>setFilter(e.target.value)}><option value='all'>All notes</option><option value='todo'>Todo</option><option value='doing'>Doing</option><option value='done'>Done</option></select><div className='note-list'>{filtered.map(n=><div key={n.id} onClick={()=>setActiveId(n.id)} className={`note-row ${activeId===n.id?'active':''}`}><strong>{n.title}</strong><span>{(n.content||'').slice(0,65)}</span></div>)}</div></aside><main className='editor'><NoteEditor active={active} onSave={save} /></main><section className='chat'><h2>Ask Local LLM</h2><textarea value={chatQ} onChange={e=>setChatQ(e.target.value)} /><button onClick={async()=>setChatA((await axios.get(`${API}/notes/chat`,{params:{q:chatQ,use_local_llm:true}})).data.answer)}>Ask</button><p>{chatA}</p></section></div>
}
createRoot(document.getElementById('root')).render(<App/>);
