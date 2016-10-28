using System.Windows;
using InterfaceWithRelay.ViewModel;
using MahApps.Metro.Controls;

namespace InterfaceWithRelay
{
    /// <summary>
    /// LoginWindow.xaml 的交互逻辑
    /// </summary>
    public partial class LoginWindow : MetroWindow
    {
        public LoginWindow()
        {
            InitializeComponent();
            this.DataContext = new LoginPageVM(this);
        }
    }
}
