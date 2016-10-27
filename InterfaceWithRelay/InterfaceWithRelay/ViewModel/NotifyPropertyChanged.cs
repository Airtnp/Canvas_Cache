using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace InterfaceWithRelay.ViewModel
{
    public class NotifyPropertyChanged : INotifyPropertyChanged
    {
        public event PropertyChangedEventHandler PropertyChanged;

        virtual internal protected void OnPropertyChanged(string propertyName)
        {
            this.PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }

        protected void SetProperty<T>(ref T storage, T value, [CallerMemberName] string propertyName = null)
        {
            if (object.Equals(storage, value)) return;

            storage = value;
            this.OnPropertyChanged(propertyName);
        }
    }
}
