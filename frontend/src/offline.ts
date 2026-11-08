export type Stored={id:string;createdAt:string;status:"queued"|"synced"|"failed"};
const DB_NAME="clinassist-offline";
const STORE_NAME="predictions";
const MAX_BATCH_SIZE=50;
function openDB():Promise<IDBDatabase>{
    return new Promise((resolve,reject)=>{
        const request=indexedDB.open(DB_NAME,1);
        request.onupgradeneeded=()=>{
            if(!request.result.objectStoreNames.contains(STORE_NAME)){
                request.result.createObjectStore(STORE_NAME,{keyPath:"id"});
            }
        };
        request.onsuccess=()=>resolve(request.result);
        request.onerror=()=>reject(request.error);
    });
}
export async function save(item:Stored):Promise<void>{
    const db=await openDB();
    try{
        await new Promise<void>((resolve,reject)=>{
            const transaction=db.transaction(STORE_NAME,"readwrite");
            transaction.objectStore(STORE_NAME).put(item);
            transaction.oncomplete=()=>resolve();
            transaction.onerror=()=>reject(transaction.error);
            transaction.onabort=()=>reject(transaction.error);
        });
    }finally{db.close();}
}
export async function all():Promise<Stored[]>{
    const db=await openDB();
    try{
        const rows=await new Promise<Stored[]>((resolve,reject)=>{
            const request=db.transaction(STORE_NAME).objectStore(STORE_NAME).getAll();
            request.onsuccess=()=>resolve(request.result);
            request.onerror=()=>reject(request.error);
        });
        return rows.sort((a,b)=>b.createdAt.localeCompare(a.createdAt));
    }finally{db.close();}
}
export async function sync():Promise<number>{
    const pending=(await all()).filter(item=>item.status==="queued"||item.status==="failed");
    if(!pending.length)return 0;
    const {api}=await import("./api");
    let totalAcknowledged=0;
    for(let start=0;start<pending.length;start+=MAX_BATCH_SIZE){
        const chunk=pending.slice(start,start+MAX_BATCH_SIZE);
        const response=await api.post("/sync/batch",{
            records:chunk.map(item=>({client_id:item.id,record_type:"prediction",created_at:item.createdAt}))
        });
        const acknowledged=new Set<string>(response.data.acknowledged_client_ids);
        for(const item of chunk){
            if(acknowledged.has(item.id)){
                await save({...item,status:"synced"});
                totalAcknowledged+=1;
            }
        }
    }
    return totalAcknowledged;
}
