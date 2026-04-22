// Package plugin defines the plugin interface for goEX
package plugin

import (
	"errors"
	"sync"
)

// Plugin defines the interface that all goEX plugins must implement
type Plugin interface {
	// Name returns the plugin name
	Name() string
	
	// Init initializes the plugin with configuration
	Init(config map[string]interface{}) error
	
	// Execute executes the plugin logic
	Execute(params map[string]interface{}) (map[string]interface{}, error)
	
	// Shutdown cleans up plugin resources
	Shutdown() error
}

// Registry manages plugin registration and lookup
type Registry struct {
	mu       sync.RWMutex
	plugins  map[string]Plugin
}

// NewRegistry creates a new plugin registry
func NewRegistry() *Registry {
	return &Registry{
		plugins: make(map[string]Plugin),
	}
}

// Register registers a plugin with the given name
func (r *Registry) Register(name string, p Plugin) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	
	if _, exists := r.plugins[name]; exists {
		return errors.New("plugin already registered: " + name)
	}
	
	r.plugins[name] = p
	return nil
}

// Get retrieves a plugin by name
func (r *Registry) Get(name string) (Plugin, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()
	
	p, exists := r.plugins[name]
	if !exists {
		return nil, errors.New("plugin not found: " + name)
	}
	
	return p, nil
}

// List returns all registered plugin names
func (r *Registry) List() []string {
	r.mu.RLock()
	defer r.mu.RUnlock()
	
	names := make([]string, 0, len(r.plugins))
	for name := range r.plugins {
		names = append(names, name)
	}
	return names
}

// Global registry instance
var GlobalRegistry = NewRegistry()

// Register is a convenience function to register plugins with the global registry
func Register(name string, p Plugin) error {
	return GlobalRegistry.Register(name, p)
}

// Get is a convenience function to get plugins from the global registry
func Get(name string) (Plugin, error) {
	return GlobalRegistry.Get(name)
}
