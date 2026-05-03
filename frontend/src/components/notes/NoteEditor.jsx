import React, { useEffect, useRef, useState } from 'react';
import axios from 'axios';

const API='http://localhost:8000';

function VoiceRecorder({noteId,onSaved}){
  const [state,setState]=useState('Idle'); const [blob,setBlob]=useState(null); const [name,setName]=useState('voice-note');
  const [duration,setDuration]=useState(0); const recRef=useRef(null); const streamRef=useRef(null); const timer=useRef(null);
  const start=async()=>{setState('Recording'); const s=await navigator.mediaDevices.getUserMedia({audio:true}); streamRef.current=s; const r=new MediaRecorder(s); const chunks=[]; r.ondataavailable=e=>chunks.push(e.data); r.onstop=()=>setBlob(new Blob(chunks,{type:r.mimeType||'audio/webm'})); r.start(); recRef.current=r; const t=Date.now(); timer.current=setInterval(()=>setDuration(Math.floor((Date.now()-t)/1000)),500)};
  const pause=()=>{if(recRef.current?.state==='recording'){recRef.current.pause();setState('Paused')}};
  const resume=()=>{if(recRef.current?.state==='paused'){recRef.current.resume();setState('Recording')}};
  const stop=()=>{setState('Processing'); recRef.current?.stop(); streamRef.current?.getTracks().forEach(t=>t.stop()); clearInterval(timer.current); setTimeout(()=>setState('Saved'),150)};
  const save=async()=>{ if(!blob) return; const file=new File([blob],`${name||'voice-note'}.webm`,{type:blob.type||'audio/webm'}); const fd=new FormData(); fd.append('file',file); await axios.post(`${API}/api/notes/${noteId}/voice-notes`,fd); onSaved();};
  return <div><h4>Voice Recorder</h4><button aria-label='start recording' onClick={start}>🎤</button><button onClick={pause}>Pause</button><button onClick={resume}>Resume</button><button onClick={stop}>Stop</button><span> {state} • {duration}s</span><div style={{height:8,background:state==='Recording'?'#ef4444':'#ddd',width:120,margin:'6px 0'}}/>{blob&&<audio controls src={URL.createObjectURL(blob)} />}<input value={name} onChange={e=>setName(e.target.value)} /><button onClick={save}>Save voice note</button></div>
}

function AttachmentCard({a,onRefresh,onInsert}){
  const run=async(path)=>{await axios.post(`${API}${path}`); onRefresh();};
  const copy=async(text)=>navigator.clipboard?.writeText(text||'');
  return <div className='att-card'>
    <strong>{a.original_filename}</strong> <small>{Math.round((a.size_bytes||0)/1024)} KB</small>
    {a.attachment_type==='audio' && <audio controls src={`${API}/${a.file_path.replace('backend/','')}`}></audio>}
    {a.attachment_type==='image' && <img src={`${API}/${a.file_path.replace('backend/','')}`} style={{maxWidth:'180px'}} />}
    {a.attachment_type==='audio' && <><button onClick={()=>run(`/api/attachments/${a.id}/transcribe`)}>Transcribe</button><small>{a.transcript_status||'idle'}</small>{a.transcript_text&&<details><summary>Transcript</summary><pre>{a.transcript_text}</pre><button onClick={()=>onInsert(a.transcript_text)}>Insert transcript into note</button><button onClick={()=>copy(a.transcript_text)}>Copy transcript</button></details>}</>}
    {a.attachment_type==='image' && <><button onClick={()=>run(`/api/attachments/${a.id}/extract-text`)}>Extract text</button><small>{a.extraction_status||'idle'}</small>{a.extracted_text&&<details><summary>Extracted text</summary><pre>{a.extracted_text}</pre><button onClick={()=>onInsert(a.extracted_text)}>Insert extracted text into note</button><button onClick={()=>copy(a.extracted_text)}>Copy extracted text</button></details>}</>}
    <button onClick={async()=>{await axios.delete(`${API}/api/attachments/${a.id}`);onRefresh();}}>Delete</button>
  </div>
}

export default function NoteEditor({active,onSave}){
  const [attachments,setAttachments]=useState([]);
  const loadA=async()=>{if(active?.id){setAttachments((await axios.get(`${API}/api/notes/${active.id}/attachments`)).data)}else setAttachments([])};
  useEffect(()=>{loadA();},[active?.id]);
  const upload=async(type,file)=>{const fd=new FormData();fd.append('file',file);fd.append('attachment_type',type); await axios.post(`${API}/api/notes/${active.id}/attachments?attachment_type=${type}`,fd); loadA();};
  if(!active) return <p className='empty'>Create or select a note.</p>;
  return <>
    <input className='title' value={active.title} onChange={e=>onSave({local:{title:e.target.value}})} onBlur={()=>onSave({title:active.title})} />
    <textarea className='content' value={active.content||''} onChange={e=>onSave({local:{content:e.target.value}})} onBlur={()=>onSave({content:active.content})} />
    <VoiceRecorder noteId={active.id} onSaved={loadA} />
    <div><input type='file' accept='image/png,image/jpeg,image/webp' onChange={e=>e.target.files?.[0]&&upload('image',e.target.files[0])}/><input type='file' accept='audio/webm,audio/wav,audio/mp3,audio/m4a' onChange={e=>e.target.files?.[0]&&upload('audio',e.target.files[0])}/></div>
    <div>{attachments.map(a=><AttachmentCard key={a.id} a={a} onRefresh={loadA} onInsert={(txt)=>onSave({content:(active.content||'')+`\n\n${txt}`})} />)}</div>
  </>
}
