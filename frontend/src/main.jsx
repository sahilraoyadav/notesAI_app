import './index.css';
import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import axios from 'axios';

const API = 'http://localhost:8000';

function App(){
  const [notes,setNotes]=useState([]);
  const [activeId,setActiveId]=useState(null);
  const [filter,setFilter]=useState('all');
  const [chatQ,setChatQ]=useState('');
  const [chatA,setChatA]=useState('');

  const load=async()=>{
    const data=(await axios.get(`${API}/notes`)).data;
    setNotes(data);
    if(data.length && !activeId) setActiveId(data[0].id);
  };

  useEffect(()=>{load();},[]);

  const active = useMemo(()=>notes.find(n=>n.id===activeId),[notes,activeId]);
  const filtered = useMemo(()=>filter==='all'?notes:notes.filter(n=>n.status===filter),[notes,filter]);

  const create=async()=>{
    const created=(await axios.post(`${API}/notes`,{title:'Untitled note',content:'',note_type:'text',status:'todo'})).data;
    await load();
    setActiveId(created.id);
  };

  const save=async(patch)=>{
    if(!active) return;
    await axios.put(`${API}/notes/${active.id}`, patch);
    await load();
  };

  const chat=async()=>setChatA((await axios.get(`${API}/notes/chat`,{params:{q:chatQ,use_local_llm:true}})).data.answer);

  return <div className='app-shell'>
    <aside className='sidebar'>
      <div className='sidebar-top'>
        <h1>NotesAI</h1>
        <button onClick={create}>+ New</button>
      </div>
      <select value={filter} onChange={e=>setFilter(e.target.value)}>
        <option value='all'>All notes</option><option value='todo'>Todo</option><option value='doing'>Doing</option><option value='done'>Done</option>
      </select>
      <div className='note-list'>
      {filtered.map(n=><div key={n.id} onClick={()=>setActiveId(n.id)} className={`note-row ${activeId===n.id?'active':''}`}>
        <strong>{n.title}</strong><span>{(n.content||'').slice(0,65)}</span>
      </div>)}
      </div>
    </aside>

    <main className='editor'>
      {active ? <>
        <input className='title' value={active.title} onChange={e=>setNotes(notes.map(n=>n.id===active.id?{...n,title:e.target.value}:n))} onBlur={()=>save({title:active.title})} />
        <textarea className='content' value={active.content||''} onChange={e=>setNotes(notes.map(n=>n.id===active.id?{...n,content:e.target.value}:n))} onBlur={()=>save({content:active.content})} placeholder='Start writing...' />
        <div className='meta'>
          <select value={active.status} onChange={e=>save({status:e.target.value})}><option value='todo'>Todo</option><option value='doing'>Doing</option><option value='done'>Done</option></select>
          <pre>{active.ai_summary||'No summary yet.'}</pre>
        </div>
      </> : <p className='empty'>Create or select a note.</p>}
    </main>

    <section className='chat'>
      <h2>Ask Local LLM</h2>
      <textarea value={chatQ} onChange={e=>setChatQ(e.target.value)} placeholder='Ask about your notes...' />
      <button onClick={chat}>Ask</button>
      <p>{chatA}</p>
    </section>
  </div>
}

createRoot(document.getElementById('root')).render(<App/>);
