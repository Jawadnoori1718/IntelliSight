// Sample data used to bring the shell to life before real detection is wired in.
// Every panel that shows this data is tagged "sample" so it's clear it's a preview.
// These get replaced by live data in later phases.

export const sampleScene = {
  description:
    'A person is working at a wooden desk, using a laptop and drinking coffee. The workspace looks organised.',
  activity: 'Working',
  environment: 'Office',
  lighting: 'Bright',
  desk: 'Organised',
  confidence: 0.97,
  objectCount: 9,
}

export const sampleObjects = [
  { id: 1, label: 'Person', sub: 'Software Developer', category: 'person', confidence: 0.97 },
  { id: 2, label: 'Laptop', sub: 'MacBook Pro 14"', category: 'tech', confidence: 0.95 },
  { id: 3, label: 'Coffee Mug', sub: 'Ceramic · ~350 ml', category: 'food', confidence: 0.88 },
  { id: 4, label: 'Keyboard', sub: 'Mechanical', category: 'tech', confidence: 0.91 },
  { id: 5, label: 'Notebook', sub: 'Open', category: 'furniture', confidence: 0.83 },
  { id: 6, label: 'Mouse', sub: 'Wireless', category: 'tech', confidence: 0.9 },
]

export const sampleTimeline = [
  { time: '10:11', label: 'Laptop', category: 'tech' },
  { time: '10:13', label: 'Coffee', category: 'food' },
  { time: '10:20', label: 'Notebook', category: 'furniture' },
  { time: '10:25', label: 'Phone', category: 'tech' },
  { time: '10:33', label: 'Passport', category: 'furniture' },
]

export const sampleMemory = [
  { time: '2:14 PM', text: 'Phone detected', where: 'Desk' },
  { time: '2:19 PM', text: 'Phone removed', where: 'Living Room · Coffee Table' },
]

export const sampleInsights = [
  { text: 'Workspace looks organised', confidence: 0.9 },
  { text: 'Two monitors detected', confidence: 0.72 },
  { text: 'Lighting is sufficient', confidence: 0.85 },
  { text: 'One notebook open', confidence: 0.8 },
]
