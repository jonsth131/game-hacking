using BepInEx;
using UnityEngine;

namespace DredgeTrainer;

[BepInPlugin(MyPluginInfo.PLUGIN_GUID, MyPluginInfo.PLUGIN_NAME, MyPluginInfo.PLUGIN_VERSION)]
public class Plugin : BaseUnityPlugin
{
    private bool _godMode;
    private bool _freezeTime;
    private bool _sanityLock;

    private void Awake()
    {
        // Plugin startup logic
        Logger.LogInfo($"Plugin {MyPluginInfo.PLUGIN_GUID} is loaded!");
    }

    private void Update()
    {
        if (_sanityLock)
        {
            GameManager.Instance.Player.Sanity.ChangeSanity(1);
        }

        if (Input.GetKeyDown(KeyCode.F1))
        {
            _godMode = !_godMode;
            typeof(Player).GetProperty("IsGodModeEnabled")!.SetValue(GameManager.Instance.Player, _godMode, null);
        }
        else if (Input.GetKeyDown(KeyCode.F2))
        {
            GameManager.Instance.Player.IsImmuneModeEnabled = !GameManager.Instance.Player.IsImmuneModeEnabled;
        }
        else if (Input.GetKeyDown(KeyCode.F3))
        {
            _freezeTime = !_freezeTime;
            GameManager.Instance.Time.ToggleFreezeTime(_freezeTime);
        }
        else if (Input.GetKeyDown(KeyCode.F4))
        {
            _sanityLock = !_sanityLock;
        }
        else if (Input.GetKeyDown(KeyCode.F5))
        {
            GameManager.Instance.PlayerAbilities.UnlockAbility("haste");
            GameManager.Instance.PlayerAbilities.UnlockAbility("spyglass");
            GameManager.Instance.PlayerAbilities.UnlockAbility("foghorn");
            GameManager.Instance.PlayerAbilities.UnlockAbility("manifest");
            GameManager.Instance.PlayerAbilities.UnlockAbility("lights");
            GameManager.Instance.PlayerAbilities.UnlockAbility("trawl");
            GameManager.Instance.PlayerAbilities.UnlockAbility("pot");
            GameManager.Instance.PlayerAbilities.UnlockAbility("banish");
            GameManager.Instance.PlayerAbilities.UnlockAbility("bait");
            GameManager.Instance.PlayerAbilities.UnlockAbility("atrophy");
            GameManager.Instance.PlayerAbilities.UnlockAbility("camera");
        }
        else if (Input.GetKeyDown(KeyCode.F6))
        {
            GameManager.Instance.AddFunds(100000);
        }
        else if (Input.GetKeyDown(KeyCode.F8))
        {
            foreach (var upgradeDate in GameManager.Instance.UpgradeManager.allUpgradeData)
            {
                GameManager.Instance.UpgradeManager.AddUpgrade(upgradeDate, true);
            }
        }
    }
}