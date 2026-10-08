# The writing standard: ASD-STE100 Simplified Technical English

Use these rules for every README and for `docs/ste-style-guide.md` in each repository. Copy this file
into the repository as `docs/ste-style-guide.md` and add a **project vocabulary** section (Section 3)
with the technical names and technical verbs of that project.

## 1. The writing rules

### Words

1. Use one word for one meaning, and one meaning for one word. Do not use synonyms for variety.
2. Use a word only as one part of speech. For example, `test` is a noun or a verb, `check` is a verb.
3. Do not use phrasal verbs (`set up`, `carry out`, `find out`, `pick up`, `look up`, `come up with`).
   Use one verb: `prepare`, `do`, `find`, `get`, `make`.
4. Do not use an `-ing` form as a noun or an adjective (`the running job`, `after indexing`).
   Exception: a technical name, a file name, a command or a status value.
5. Do not use contractions (`don't`, `it's`, `can't`). Do not use slang or idioms
   (`out of the box`, `under the hood`, `at a glance`, `gotcha`, `bells and whistles`).
6. Do not use `and/or`. Write `A, B or both`.
7. Do not use `should`, `could`, `would` or `may` for instructions. Use `must` for a rule, the
   imperative for a step and `can` for a possibility.
8. Keep the articles `a`, `an` and `the` in sentences.
9. Do not make a noun cluster of more than three words. A technical name is one word.

### Sentences

1. A procedural sentence (an instruction) has a maximum of **20 words**.
2. A descriptive sentence has a maximum of **25 words**.
3. Write one instruction in one sentence.
4. Use the imperative for an instruction: `Run the tests.` Not `The tests should be run.`
5. Use the active voice. Use the passive voice only when the agent of the action is not important.
6. Use only the simple present, the simple past and the simple future.
7. Put a condition before the instruction: `If the index is stale, build it again.`
8. Do not use semicolons in sentences. Write two sentences.

### Paragraphs, notes and warnings

1. A paragraph has one topic and a maximum of **6 sentences**. Start with the topic sentence.
2. A warning or a caution starts with a clear command. Then it gives the reason.
3. A note gives information. It does not give an instruction.
4. Use a vertical list for a sequence or a set of conditions. Each item of a numbered procedure is one step.

### Tables, headings and diagrams

1. A table cell can be a short phrase. If a cell has a sentence, the sentence obeys the rules.
2. A heading is a noun phrase (`The cost model`) or an imperative (`Run the demo`).
   Do not start a heading with an `-ing` form.
3. A diagram label is a short phrase. Use the same terms as the text.

### What STE does not change

Code, commands, file names, paths, field names, environment variables, status values, enum values,
product names and URLs stay exactly as they are. They are technical names. Put them in backticks.

## 2. General words to replace

| Do not use | Use |
|---|---|
| utilize, leverage | use |
| in order to | to |
| set up | prepare, install, configure |
| carry out, perform | do |
| make sure, ensure | make sure (allowed), or `check that` |
| a lot of, lots of | many, much |
| e.g., i.e. | for example, that is |
| should (instruction) | must (rule) / imperative (step) |
| might, may (possibility) | can |
| very, really, just, simply, easily | (delete) |
| seamless, robust, powerful, blazing | (delete or give a measured fact) |

## 3. Project vocabulary

This section gives the technical names and the technical verbs of MedXpert. The README uses each term with only this meaning.

### 3.1 Technical names (nouns)

| Term | Meaning | Do not use |
|---|---|---|
| **message** | One text that the user types in the chat input | prompt (for user text), utterance |
| **route** | The path of a message after the classifier: `general_chat` or `symptom_query` | intent, flow, branch |
| **classifier** | The GPT-4 prompt `classify_input_type` | MCP, router, RoutingAgent |
| **symptom query** | A message on the `symptom_query` route | medical question, health query |
| **general chat** | A message on the `general_chat` route | small talk route, casual query |
| **clinical phrase** | The keyword that `rephrase_symptom_for_sql` returns | interpreted symptom (except the UI label), normalized query |
| **SQL agent** | The function `generate_sql_query` | text-to-SQL model, query bot |
| **LLM agent** | The module `agents/llm_agent.py` | assistant module, GPT layer |
| **medicines table** | The PostgreSQL table `medicines_table` | drug database, medicine DB |
| **medicine card** | The HTML block of one medicine in a reply | tile, result box |
| **summary** | The GPT-4 text that explains one medicine to a patient | description, explanation (as a noun for this text) |
| **user manual** | The 8-part text from the manual page | leaflet, guide, instructions file |
| **sample row** | The fixed medicine data in `pages/1_User_Manual.py` | dummy row (except the variable name `dummy_row`), mock |
| **collection** | A named set of vectors in Qdrant or ChromaDB | index, table (for vectors) |
| **embedding** | The 384-number vector of a text from `all-MiniLM-L6-v2` | encoding, feature vector |
| **payload** | The fields stored with a Qdrant vector | metadata (for Qdrant) |
| **SPL archive** | One DailyMed ZIP file with XML and label images | package, bundle |
| **text record** | One `output/records/<id>.txt` file | document, dump |
| **OCR text** | The text that Tesseract reads from a label image | scan text, extracted content |

### 3.2 Technical verbs

| Verb | Meaning |
|---|---|
| **classify** | Give a message its route |
| **rewrite** | Change a symptom into a clinical phrase |
| **generate** | Get SQL, a reply, a summary or a user manual from GPT-4 |
| **query** | Run SQL on the medicines table |
| **summarize** | Write a patient-level summary of one medicine row |
| **encode** | Change a text into an embedding |
| **search** | Find the nearest embeddings in a collection |
| **ingest** | Read SPL archives and add their points to Qdrant |
| **extract** | Copy the files of an SPL archive into a temporary folder |
